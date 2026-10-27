# neerajk.github.io

Personal portfolio of **Neeraj Karoshi**, Geospatial AI Engineer, built with [Astro](https://astro.build) and hosted on GitHub Pages.

The site is styled like a satellite scene:

- **Band switcher** (header, or keys `1`–`5`) recolours the whole site as RGB true colour, NIR false colour, SAR backscatter, TIR thermal or PAN (light mode).
- **Pixel Observatory** in the hero: real 3.2 × 3.2 km tiles (10 m) of Bengaluru, Enschede and Dehradun.
  - Layers: Sentinel-2 true and false colour, NDVI, ΔNDVI (change since the first year), ESA WorldCover land cover, Sentinel-1 VV backscatter and Landsat land surface temperature.
  - **Time slider** with play button: the same season in several years, all with one shared colour stretch, so visible differences are real change.
  - A crosshair follows the cursor (or arrow keys) and reads out date, lat/lon, class, NDVI, ΔNDVI, VV dB and LST °C. The band switcher also picks the matching layer.
- **Ground track**: the career path drawn over a world basemap with a sun-synchronous orbit (i = 98.6°). Land outlines come from [Natural Earth](https://www.naturalearthdata.com/) 1:110m (public domain) via [world-atlas](https://github.com/topojson/world-atlas) 2.0.2 (ISC), pre-projected into `src/data/land.ts`.
- **Acquisitions**: work and study as an archive-coverage chart.
- **Spectral bands**: skills grouped as bands.

No UI framework and no client-side dependencies: only Astro and a few small inline scripts.

## Edit content

All text lives in [`src/data/cv.ts`](src/data/cv.ts). Update it when the CV changes, and replace `public/Neeraj_Karoshi_CV.pdf` with the new PDF.

To add a project, append an entry to `projects` and pick a `glyph`: `roads`, `lulc`, `canopy`, `flood` or `graph`. Add `url` to make the card a link.

## Regenerate the Pixel Observatory tiles

The tiles are produced once, offline, from Microsoft Planetary Computer (no account needed) and committed:

```bash
pip install -r tools/requirements.txt
python tools/make_aoi_tiles.py
```

This writes `public/aoi/<place>/{vis,dat,dat2}.png` and `src/data/aois.json`. Edit the `AOIS` list at the top of the script to move a tile or change its date window. Data: Copernicus Sentinel-2 and Sentinel-1 (modified Copernicus data), Landsat courtesy of the U.S. Geological Survey, ESA WorldCover 2021 (CC BY 4.0).

## Run locally

Requires Node 22.23.4+ (Astro 7). The deploy workflow builds with Node 24.

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # static site in dist/
npm run preview
```

## Deploy

1. Create a public repo named **`neerajk.github.io`** and push to `main`.
2. In the repo, open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Each push to `main` runs `.github/workflows/deploy.yml` and publishes to https://neerajk.github.io.

To host it under a different repo name instead (for example `portfolio`), add `base: '/portfolio'` in `astro.config.mjs`. The site is then served at `https://neerajk.github.io/portfolio/`, and the root-relative links (`/favicon.svg`, `/Neeraj_Karoshi_CV.pdf`) need the same prefix.

## Content

Text, CV and images © Neeraj Karoshi.
