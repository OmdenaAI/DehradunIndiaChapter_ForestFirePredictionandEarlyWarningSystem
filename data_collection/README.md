# Data Collection

This repository contains the scripts and Jupyter notebooks required for data collection, covering both static and dynamic features. The data collected will be used for analysis, modeling, or further processing. This README provides details on the structure of the repository, usage instructions, and dependencies.

## Table of Contents

1. [Overview](#overview)
2. [Repository Structure](#repository-structure)
3. [Setup Instructions](#setup-instructions)
4. [Static Features](#static-features)
    - [Purpose](#purpose)
    - [List of Static Features](#list-of-static-features)
    - [Usage](#usage)
5. [Dynamic Features](#dynamic-features)
    - [Purpose](#purpose)
    - [List of Dynamic Features](#list-of-dynamic-features)
    - [Usage](#usage)
6. [Dependencies](#dependencies)
7. [Contributing](#contributing)
8. [License](#license)

---

## Overview

This repository is organized to streamline the process of downloading and organizing data. The scripts are categorized into two main types:

- **Static Features**: Features that do not change over time (e.g., geographic information, demographics).
- **Dynamic Features**: Features that change with time (e.g., weather data, vegetation indices).

---

## Repository Structure

```
|-- data_collection
    |-- notebooks
        |-- FPAR_and_LAI_download.ipynb
        |-- MODIS_Burned_area_Data_Collection_and_EDA_2024.ipynb
        |-- Population_density_UK_2020.ipynb
        |-- Uttarakhand_LST1.ipynb
        |-- Uttarakhand_land_cover_2012_2023.ipynb
        |-- rasterResampling.ipynb
    |-- scripts
        |-- process_era5land.py
    |-- README.md
```

- **notebooks/**: Contains Jupyter notebooks for data download,resampling.
- **scripts/**: Contains Python scripts for automated or command-line data collection.
---

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/OmdenaAI/DehradunIndiaChapter_ForestFirePredictionandEarlyWarningSystem.git
   cd data_collection
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API keys or data source credentials if required. Instructions for specific sources are provided in the scripts/notebooks.

---

## Static Features

### Purpose

Static features include data that remains constant over time. Examples:
- Geographic boundaries
- Population demographics
- Infrastructure data

### List of Static Features

1. Land Cover
2. Elevation
3. Aspect
4. Slope
5. Population Density

### Usage

1. **Notebook**:
   Open and run `notebooks/static_features/download_static_features.ipynb` using Jupyter or a similar environment.

   ```bash
   jupyter notebook notebooks/static_features/download_static_features.ipynb
   ```

2. **Script**:
   Run the script for static data download:
   ```bash
   python scripts/static_features/static_features_download.py
   ```

---

## Dynamic Features

### Purpose

Dynamic features include data that changes over time. Examples:
- Weather data
- Vegetation indices
- Sensor readings

### List of Dynamic Features

**Vegetation Data:**
1. Fraction of photosynthetically active radiation
2. Leaf area index
3. Normalized difference vegetation index (NDVI)
4. Enhanced vegetation index (EVI)
5. Evapotranspiration
6. Potential evapotranspiration

**Weather Data:**
1. Daytime land surface temperature
2. Nighttime land surface temperature
3. The max value of the eastward component of the 10 m wind
4. The max value of the northward component of the 10 m wind
5. Max atmospheric temperature
6. Max precipitation
7. The min value of the eastward component of the 10 m wind
8. The min value of the northward component of the 10 m wind
9. Min atmospheric temperature
10. Min precipitation

### Usage

1. **Notebook**:
   Open and run `notebooks/dynamic_features/download_dynamic_features.ipynb` using Jupyter or a similar environment.

   ```bash
   jupyter notebook notebooks/dynamic_features/download_dynamic_features.ipynb
   ```

2. **Script**:
   Run the script for dynamic data download:
   ```bash
   python scripts/dynamic_features/dynamic_features_download.py
   ```

---

## Dependencies

Ensure the following dependencies are installed:

- Python 3.8+
- Jupyter Notebook
- pandas
- numpy
- requests
- Any other libraries specified in `requirements.txt`

---

## Contributing

Contributions are welcome! If you want to add features, fix bugs, or improve the documentation:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.

---

## License

This repository is licensed under the MIT License. See the `LICENSE` file for details.

---


