#!/usr/bin/env python3
"""Build the Pixel Observatory tiles shown in the hero.

For each AOI this cuts an N x N grid at 10 m in the local UTM zone. For every year in
the AOI's list it takes the clearest scene from the same season (so the time slider shows
change, not phenology) and writes three PNGs to public/aoi/<slug>/<year>/:

  vis.png   RGB = Sentinel-2 L2A B04, B03, B02 (2-98 % stretch shared by all years)
  dat.png   RGB = [B08 stretched, NDVI encoded, ESA WorldCover class code]
  dat2.png  RGB = [Sentinel-1 RTC VV encoded, Landsat LST encoded, validity flags]

Metadata goes to src/data/aois.json.

Encodings (decoded in src/components/PixelObservatory.astro):
  NDVI = G / 127.5 - 1
  VV   = R / 255 * 35 - 30      dB, clipped to -30..5
  LST  = G / 255 * 70 - 10      deg C, clipped to -10..60
  flags (B of dat2): 1 = Sentinel-2 clear, 2 = Sentinel-1 valid, 4 = LST valid

Data comes from Microsoft Planetary Computer (anonymous, signed URLs).
Run it once, check the PNGs, then commit public/aoi/ and src/data/aois.json:

    pip install -r tools/requirements.txt
    python tools/make_aoi_tiles.py
"""

from __future__ import annotations

import json
import shutil
from collections import defaultdict
from pathlib import Path

import numpy as np
import odc.stac
import planetary_computer
import pystac_client
from odc.geo.geobox import GeoBox
from PIL import Image
from pyproj import Transformer

N = 320  # pixels per side
RES = 10  # metres
MIN_CLEAR = 0.9  # skip a year if less than this share of the tile is cloud-free
ROOT = Path(__file__).resolve().parents[1]
PC = "https://planetarycomputer.microsoft.com/api/stac/v1"

# Centre points, the season to sample (MM-DD start, MM-DD end; an end before the start
# runs into the next year) and the years on the time slider.
AOIS = [
    {"slug": "bengaluru", "name": "Bengaluru", "lat": 12.9760, "lon": 77.6020,
     "season": ("01-01", "03-31"), "years": [2019, 2021, 2023, 2026]},
    {"slug": "enschede", "name": "Enschede", "lat": 52.2310, "lon": 6.8730,
     "season": ("05-01", "08-31"), "years": [2019, 2021, 2023, 2026]},
    {"slug": "dehradun", "name": "Dehradun", "lat": 30.3380, "lon": 78.0300,
     "season": ("10-15", "02-28"), "years": [2019, 2021, 2023, 2025]},
]

S2_CLEAR = [2, 4, 5, 6, 7, 11]  # SCL: dark area, vegetation, not-vegetated, water, unclassified, snow
LANDSAT_CLOUD_BITS = 0b11110  # QA_PIXEL bits 1-4: dilated cloud, cirrus, cloud, cloud shadow


def season_window(year: int, season: tuple[str, str]) -> str:
    start, end = season
    end_year = year if end >= start else year + 1
    return f"{year}-{start}/{end_year}-{end}"


def utm_epsg(lat: float, lon: float) -> int:
    zone = int((lon + 180) // 6) + 1
    return (32600 if lat >= 0 else 32700) + zone


def make_grid(aoi: dict) -> tuple[GeoBox, int, list[float], dict]:
    epsg = utm_epsg(aoi["lat"], aoi["lon"])
    x, y = Transformer.from_crs(4326, epsg, always_xy=True).transform(aoi["lon"], aoi["lat"])
    x, y = round(x / RES) * RES, round(y / RES) * RES  # align with the 10 m Sentinel-2 grid
    h = N * RES / 2
    gbox = GeoBox.from_bbox((x - h, y - h, x + h, y + h), crs=f"epsg:{epsg}", shape=(N, N))
    inv = Transformer.from_crs(epsg, 4326, always_xy=True)
    corners = {
        "nw": inv.transform(x - h, y + h),
        "ne": inv.transform(x + h, y + h),
        "sw": inv.transform(x - h, y - h),
        "se": inv.transform(x + h, y - h),
    }
    lons = [c[0] for c in corners.values()]
    lats = [c[1] for c in corners.values()]
    bbox = [min(lons), min(lats), max(lons), max(lats)]
    return gbox, epsg, bbox, {k: [round(v[0], 6), round(v[1], 6)] for k, v in corners.items()}


def search(cat, collection: str, bbox: list[float], window: str, **kw) -> list:
    return list(cat.search(collections=[collection], bbox=bbox, datetime=window, **kw).items())


def need(items: list, what: str, aoi: dict, window: str) -> list:
    if not items:
        raise RuntimeError(f"No {what} found for {aoi['name']} in {window}; widen the window.")
    return items


def by_day(items: list) -> list[list]:
    """Group items by acquisition date, least cloudy day first."""
    days = defaultdict(list)
    for it in items:
        days[it.datetime.date()].append(it)
    return sorted(days.values(), key=lambda its: min(i.properties.get("eo:cloud_cover", 100) for i in its))


def load(items: list, bands: list[str], gbox: GeoBox) -> dict[str, np.ndarray]:
    ds = odc.stac.load(
        items,
        bands=bands,
        geobox=gbox,
        groupby="solar_day",
        resampling={"*": "bilinear", "SCL": "nearest", "qa_pixel": "nearest", "map": "nearest"},
    ).isel(time=0)
    return {b: ds[b].values for b in bands}


def stretch(a: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return np.nan_to_num(np.clip((a - lo) / (hi - lo), 0, 1) * 255).astype(np.uint8)


def sentinel2(cat, aoi, window, bbox, gbox):
    items = search(cat, "sentinel-2-l2a", bbox, window, query={"eo:cloud_cover": {"lt": 30}})
    best = None
    for its in by_day(need(items, "Sentinel-2", aoi, window))[:10]:
        scl = load(its, ["SCL"], gbox)["SCL"]
        frac = float(np.isin(scl, S2_CLEAR).mean())
        if best is None or frac > best[1]:
            best = (its, frac, scl)
        if frac >= 0.98:
            break
    its, frac, scl = best
    b = load(its, ["B02", "B03", "B04", "B08"], gbox)
    # Processing baseline 04.00+ (from 2022-01-25) adds a +1000 DN offset to L2A reflectance.
    baseline = float(its[0].properties.get("s2:processing_baseline", "0"))
    offset = 1000 if baseline >= 4 else 0
    refl = {}
    for k, v in b.items():
        v = v.astype("float32")
        v[v == 0] = np.nan
        refl[k] = (v - offset) / 10000
    clear = np.isin(scl, S2_CLEAR) & np.isfinite(refl["B04"])
    info = {"date": str(its[0].datetime.date()), "id": its[0].id, "clear": round(frac, 3), "baseline": f"{baseline:05.2f}"}
    return refl, clear, info


def sentinel1(cat, aoi, window, bbox, gbox):
    items = need(search(cat, "sentinel-1-rtc", bbox, window), "Sentinel-1 RTC", aoi, window)
    its = sorted(by_day(items), key=lambda its: its[0].datetime, reverse=True)[0]
    vv = load(its, ["vv"], gbox)["vv"].astype("float32")
    valid = np.isfinite(vv) & (vv > 0)
    db = np.where(valid, 10 * np.log10(np.where(valid, vv, 1)), np.nan)
    return db, valid, {"date": str(its[0].datetime.date()), "id": its[0].id}


def landsat_lst(cat, aoi, window, bbox, gbox):
    items = search(
        cat, "landsat-c2-l2", bbox, window,
        query={"eo:cloud_cover": {"lt": 30}, "platform": {"in": ["landsat-8", "landsat-9"]}},
    )
    best = None
    for its in by_day(need(items, "Landsat", aoi, window))[:8]:
        qa = load(its, ["qa_pixel"], gbox)["qa_pixel"].astype("uint16")
        ok = ((qa & LANDSAT_CLOUD_BITS) == 0) & ((qa & 1) == 0)
        if best is None or ok.mean() > best[1].mean():
            best = (its, ok)
        if ok.mean() >= 0.98:
            break
    its, ok = best
    st = load(its, ["lwir11"], gbox)["lwir11"].astype("float32")
    valid = ok & (st > 0)
    # Collection 2 Level-2 surface temperature: K = DN * 0.00341802 + 149.0
    lst = np.where(valid, st * 0.00341802 + 149.0 - 273.15, np.nan)
    info = {"date": str(its[0].datetime.date()), "id": its[0].id, "platform": its[0].properties.get("platform")}
    return lst, valid, info


def worldcover(cat, bbox, gbox):
    items = search(cat, "esa-worldcover", bbox, "2021-01-01/2021-12-31")
    if not items:
        raise SystemExit("No ESA WorldCover 2021 tile found.")
    return load(items, ["map"], gbox)["map"].astype("uint8")


def optional(fn, label, *args):
    """SAR and thermal are optional: if a source fails, its layer shows 'no data'."""
    try:
        arr, ok, info = fn(*args)
        print(f"    {label} {info['date']}")
        return arr, ok, info
    except Exception as e:  # noqa: BLE001
        print(f"    {label} skipped: {e}")
        return np.full((N, N), np.nan, "float32"), np.zeros((N, N), bool), None


def build_aoi(cat, aoi: dict) -> dict:
    print(f"[{aoi['name']}]")
    gbox, epsg, bbox, corners = make_grid(aoi)
    lc = worldcover(cat, bbox, gbox)

    epochs = []
    for year in aoi["years"]:
        window = season_window(year, aoi["season"])
        print(f"  {year}  ({window})")
        try:
            refl, clear, s2 = sentinel2(cat, aoi, window, bbox, gbox)
        except RuntimeError as e:
            print(f"    skipped: {e}")
            continue
        if s2["clear"] < MIN_CLEAR:
            print(f"    skipped: best Sentinel-2 scene only {s2['clear']:.0%} clear")
            continue
        print(f"    S2 {s2['date']} clear={s2['clear']}")
        db, s1_ok, s1 = optional(sentinel1, "S1", cat, aoi, window, bbox, gbox)
        lst, lst_ok, ls = optional(landsat_lst, "Landsat", cat, aoi, window, bbox, gbox)
        epochs.append({"key": str(year), "refl": refl, "clear": clear, "s2": s2,
                       "db": db, "s1_ok": s1_ok, "s1": s1, "lst": lst, "lst_ok": lst_ok, "ls": ls})
    if not epochs:
        raise SystemExit(f"No usable years for {aoi['name']}.")

    # One stretch for all years, so colour differences on the slider are real differences.
    rgb_px = np.concatenate([np.stack([e["refl"][b][e["clear"]] for b in ("B04", "B03", "B02")]).ravel() for e in epochs])
    lo, hi = np.nanpercentile(rgb_px, [2, 98])
    nir_px = np.concatenate([e["refl"]["B08"][e["clear"]] for e in epochs])
    nlo, nhi = np.nanpercentile(nir_px, [2, 98])
    lst_px = [e["lst"][e["lst_ok"]] for e in epochs if e["lst_ok"].any()]
    lst_range = [round(float(v), 1) for v in np.nanpercentile(np.concatenate(lst_px), [2, 98])] if lst_px else None

    out = ROOT / "public" / "aoi" / aoi["slug"]
    shutil.rmtree(out, ignore_errors=True)
    meta_epochs = []
    for e in epochs:
        r = e["refl"]
        vis = stretch(np.stack([r["B04"], r["B03"], r["B02"]], -1), lo, hi)
        nir = stretch(r["B08"], nlo, nhi)
        ndvi = (r["B08"] - r["B04"]) / (r["B08"] + r["B04"] + 1e-6)
        ndvi_enc = np.nan_to_num(np.clip((ndvi + 1) * 127.5, 0, 255)).astype(np.uint8)
        vv_enc = np.nan_to_num(np.clip((e["db"] + 30) / 35 * 255, 0, 255)).astype(np.uint8)
        lst_enc = np.nan_to_num(np.clip((e["lst"] + 10) / 70 * 255, 0, 255)).astype(np.uint8)
        flags = (e["clear"] * 1 + e["s1_ok"] * 2 + e["lst_ok"] * 4).astype(np.uint8)

        d = out / e["key"]
        d.mkdir(parents=True, exist_ok=True)
        Image.fromarray(vis, "RGB").save(d / "vis.png", optimize=True)
        Image.fromarray(np.stack([nir, ndvi_enc, lc], -1), "RGB").save(d / "dat.png", optimize=True)
        Image.fromarray(np.stack([vv_enc, lst_enc, flags], -1), "RGB").save(d / "dat2.png", optimize=True)
        meta_epochs.append({"key": e["key"], "s2": e["s2"], "s1": e["s1"], "lst": e["ls"]})

    return {
        "slug": aoi["slug"], "name": aoi["name"], "n": N, "res": RES, "epsg": epsg,
        "corners": corners, "lst_range": lst_range, "lc": {"source": "ESA WorldCover 2021 v200"},
        "epochs": meta_epochs,
    }


def main() -> None:
    cat = pystac_client.Client.open(PC, modifier=planetary_computer.sign_inplace)
    meta = [build_aoi(cat, aoi) for aoi in AOIS]
    (ROOT / "src" / "data" / "aois.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("Wrote", ROOT / "src" / "data" / "aois.json")


if __name__ == "__main__":
    main()
