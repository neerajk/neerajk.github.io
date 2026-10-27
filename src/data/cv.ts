// Single source of truth for the site. Edit this file when the CV changes.

export const profile = {
  name: 'Neeraj Karoshi',
  role: 'Geospatial AI Engineer',
  tags: ['Computer Vision', 'Remote Sensing & GIS', 'Foundation Models'],
  email: 'neerajvkaroshi@gmail.com',
  github: 'https://github.com/neerajk',
  linkedin: 'https://www.linkedin.com/in/neerajkaroshi/',
  cv: '/Neeraj_Karoshi_CV.pdf',
  bases: ['Enschede, Netherlands', 'Dehradun, India'],
  summary:
    'MSc student in GIS & Earth Observation with around 2.5 years of experience in large-scale data processing, EDA, machine learning and computer vision. I build end-to-end AI pipelines for satellite imagery: semantic segmentation, LULC change detection and canopy height estimation, with PyTorch, GDAL and LangGraph, plus the ETL, MLOps and foundation-model work that gets them into production.',
};

// Career "ground track". Coordinates are city centres, WGS84 (lat, lon).
export const stations = [
  { id: 'BLR', place: 'Bengaluru', lat: 12.97, lon: 77.59, when: '2017', what: 'BE Computer Science' },
  { id: 'BOM', place: 'Mumbai', lat: 19.08, lon: 72.88, when: '2021', what: 'Software Developer, IIFL' },
  { id: 'VMN', place: 'Vermillion, SD', lat: 42.78, lon: -96.93, when: '2022', what: 'Graduate Assistant, USD' },
  { id: 'NYC', place: 'New York', lat: 40.71, lon: -74.01, when: '2023', what: 'Data Analyst Intern, UNDP' },
  { id: 'DEL', place: 'Delhi', lat: 28.61, lon: 77.21, when: '2023', what: 'PG Diploma CS & AI, IIIT Delhi' },
  { id: 'HYD', place: 'Hyderabad', lat: 17.39, lon: 78.49, when: '2023', what: 'Data Analyst, Transoft' },
  { id: 'DDN', place: 'Dehradun', lat: 30.32, lon: 78.03, when: '2025', what: 'MSc GIS & EO, IIRS (ISRO)' },
  { id: 'ENS', place: 'Enschede', lat: 52.22, lon: 6.89, when: '2025', what: 'MSc GIS & EO, ITC, University of Twente' },
];

export const experience = [
  {
    title: 'Data Analyst',
    org: 'Transoft Solutions',
    short: 'Transoft',
    place: 'Hyderabad, India',
    from: '11/2023',
    to: '07/2025',
    points: [
      'Architected scalable ETL and analytics pipelines with Python, Pandas, SQL and scikit-learn for large enterprise datasets.',
      'Developed supervised ML models for predictive analytics, operational optimisation and automated decision support.',
      'Worked with engineering and business teams to optimise database operations and analytics infrastructure.',
    ],
  },
  {
    title: 'Data Analyst Intern',
    org: 'United Nations Development Programme (UNDP)',
    short: 'UNDP',
    place: 'New York, USA',
    from: '08/2023',
    to: '10/2023',
    points: [
      'Automated economic-intelligence workflows through API integrations, web scraping and ingestion pipelines.',
      'Ran EDA, statistical modelling and regression analysis on multinational development datasets.',
      'Built reproducible analytics workflows for policy reporting and visualisation.',
    ],
  },
  {
    title: 'Graduate Assistant',
    org: 'University of South Dakota',
    short: 'Univ. of South Dakota',
    place: 'Vermillion, USA',
    from: '08/2022',
    to: '12/2022',
    points: [
      'Research and teaching assignments; guided undergraduates through projects and machine-learning concepts.',
      'Explored Kernel Change Point Detection with CNNs and RNNs, using CUDA GPU acceleration for time-series segmentation and anomaly detection.',
    ],
  },
  {
    title: 'Software Developer',
    org: 'IIFL Finance',
    short: 'IIFL Finance',
    place: 'Mumbai, India',
    from: '09/2021',
    to: '01/2022',
    points: [
      'Streamlined ETL and CRM automation workflows, improving operational reporting efficiency.',
      'Developed internal dashboards and automation utilities for business intelligence.',
    ],
  },
];

export const education = [
  {
    degree: 'MSc Geo-information Science & Earth Observation (Geoinformatics)',
    short: 'MSc GIS & EO',
    orgs: [
      'Indian Institute of Remote Sensing (IIRS), ISRO, Dehradun',
      'ITC Faculty, University of Twente, Enschede',
    ],
    when: '09/2025 – present',
  },
  {
    degree: 'Post Graduate Diploma in Computer Science & AI',
    short: 'PG Diploma · IIIT Delhi',
    orgs: ['IIIT Delhi'],
    when: '2023 – 2024',
  },
  {
    degree: 'BE Computer Science & Engineering',
    short: 'BE · VTU',
    orgs: ['Sir M. Visvesvaraya Institute of Technology, VTU, Bengaluru'],
    when: '2017 – 2021',
  },
];

// `glyph` picks the generative thumbnail drawn for each project tile.
export const projects = [
  {
    name: 'Road Extraction from LISS-IV',
    sensor: 'LISS-IV',
    gsd: '5.8 m',
    task: 'Segmentation',
    glyph: 'roads',
    text: 'Testing whether roads can be extracted automatically from 5.8 m LISS-IV imagery, with deep-learning segmentation pipelines built for difficult medium-resolution data.',
  },
  {
    name: 'LULC with the CLAY Foundation Model',
    sensor: 'Sentinel-2',
    gsd: '10 m',
    task: 'Classification',
    glyph: 'lulc',
    text: 'Fine-tuned CLAY for land-use/land-cover classification on Sentinel-2 imagery using transfer learning.',
  },
  {
    name: 'Canopy Height via DINOv3',
    sensor: 'High-res optical',
    gsd: 'High-res',
    task: 'Regression',
    glyph: 'canopy',
    text: 'A canopy height estimation pipeline that uses the DINOv3 foundation model to extract features from high-resolution satellite imagery.',
  },
  {
    name: 'Flood Mapping with Sentinel-1',
    sensor: 'Sentinel-1 SAR',
    gsd: '10 m',
    task: 'Change detection',
    glyph: 'flood',
    text: 'End-to-end SAR flood mapping: speckle filtering, change detection and inundation analysis.',
  },
  {
    name: 'GeoAI-Kit',
    sensor: 'Claude Code / Codex',
    gsd: '11 domains',
    task: 'Agent skills',
    glyph: 'graph',
    url: 'https://github.com/neerajk/geoai-kit',
    text: 'An open-source geospatial AI toolkit of reusable, evidence-tagged workflows for remote sensing and GIS, used as a skill in Claude Code and Codex.',
  },
];

export const achievements = [
  {
    title: 'Winner, Space & Water Nexus Hackathon',
    org: 'SATUrN Tech',
    when: 'October 2026',
    text: 'Contributed to BruinRadar, a geospatial decision-support prototype that combines satellite remote sensing, field boundaries, elevation and rainfall to flag potentially flooded potato fields and assess brown rot risk.',
  },
];

// Skills rendered as spectral "bands".
export const bands = [
  { code: 'B01', name: 'Programming', items: ['Python', 'C/C++', 'SQL', 'Shell'] },
  {
    code: 'B02',
    name: 'AI & Deep Learning',
    items: ['PyTorch', 'TensorFlow/Keras', 'scikit-learn', 'Computer Vision', 'Transfer Learning', 'Semantic Segmentation', 'Change Detection', 'Vision Transformers', 'CLAY', 'DINOv3'],
  },
  {
    code: 'B03',
    name: 'Geospatial & Remote Sensing',
    items: ['GDAL', 'Rasterio', 'GeoPandas', 'Xarray', 'rioxarray', 'PostGIS', 'QGIS', 'ArcGIS', 'Google Earth Engine', 'Sentinel-1 SAR', 'Sentinel-2', 'Optical/SAR processing'],
  },
  {
    code: 'B04',
    name: 'EO Data Engineering',
    items: ['STAC APIs', 'Planetary Computer', 'stackstac', 'odc-stac', 'Dask', 'Data cubes', 'Raster/vector pipelines'],
  },
  { code: 'B05', name: 'AI Workflow Engineering', items: ['LangChain', 'LangGraph', 'LLM tool orchestration'] },
  { code: 'B06', name: 'Development', items: ['Git', 'Docker', 'Linux', 'Streamlit', 'REST APIs', 'Web scraping'] },
];
