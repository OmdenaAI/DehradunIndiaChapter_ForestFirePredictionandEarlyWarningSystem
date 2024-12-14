"""
Inputs to this script are locally downloaded ERA5-Land hourly data in GRIB format.
ERA5-Land data use the WGS 1984 coordinate reference frame.
Data download link: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land

For each day covered in the GRIB data, this script outputs GeoTiff files of:
- 2 m temperature,
- 10 m u-component (horizontal component) of wind,
- 10 m v-component (vertical component) of wind, and
- Total precipitation.

Tasks performed in script:
1. Upsample data variables from 9 km native resolution to 500 m spatial resolution.
2. Aggregate data from hourly resolution to daily estimates using min, max, and sum.
3. Clip upsampled data to the spatial extent of Uttarakhand shapefile.

Assumption:
The Uttarakhand shapefile uses WGS 1984 coordinates.

File author: Akshay Suresh
"""

import os
import time
from pathlib import Path
import glob
import numpy as np
import pandas as pd
import xarray as xr
import rioxarray as rxr

# FILES and DATA VARIABLES
ERA5_DATA_PATH = Path("../ERA5")
UTTARAKHAND_RASTER = "../Shapefiles/uttarakhand_WGS1984.tif"
OUTPUT_PATH = Path("../era5land_data")
# Variables: 2-meter temperature, 10-meter u- and v-components of wind, total precipitation
DATA_VARS = ["t2m", "u10", "v10", "tp"]
# Specify if any of the above data variables are accumulated or cumulative quantities.
ACCUMULATED_VARS = {"tp"}
# Native spatial resolution (m) of ERA5-Land hourly data
ERA5_NATIVE_RESOL = 9000
# Desired spatial resolution (m)
DESIRED_RESOL = 500

# Determine scale factor for upsampling.
SCALE_FACTOR = int(ERA5_NATIVE_RESOL / DESIRED_RESOL)
if SCALE_FACTOR <= 1:
    print("Scale factor <= 1. Data upsampling will not be performed.")

#########################################################################################
# FUNCTION DEFINITIONS


def upsample_data(
    data_arr: xr.DataArray, lat_factor: int, lon_factor: int
) -> xr.DataArray:
    """
    Perform linear interpolation to upsample a data array.

    Args:
        data_arr: Input data array
        lat_factor: Upsampling factor along latitude axis
        lon_factor: Upsampling factor along longitude axis

    Returns: Upsampled data array
    """
    # Create upsampled latitude axis.
    n_lat = lat_factor * (len(data_arr.latitude) - 1) + 1
    lat_new = np.linspace(
        data_arr.latitude.values[0], data_arr.latitude.values[-1], n_lat
    )

    # Create upsampled longitude axis.
    n_lon = lon_factor * (len(data_arr.longitude) - 1) + 1
    lon_new = np.linspace(
        data_arr.longitude.values[0], data_arr.longitude.values[-1], n_lon
    )

    # Upsample data array.
    data_arr_upsampled = data_arr.interp(
        latitude=lat_new, longitude=lon_new, method="linear"
    )
    return data_arr_upsampled


#########################################################################################
# Start time of code execution
start_time = time.time()

# Load rasterized shapefile mask into memory.
shp_mask = rxr.open_rasterio(UTTARAKHAND_RASTER, decode_coords="all")
shp_mask = xr.DataArray(
    shp_mask[0].values.copy(),
    dims=["latitude", "longitude"],
    coords={
        "latitude": shp_mask["y"].values.copy(),
        "longitude": shp_mask["x"].values.copy(),
    },
)

# Gather list of .grib files located at ERA5_DATA_PATH.
grib_file_list = sorted(glob.glob(str(ERA5_DATA_PATH / "*.grib")))

# Loop over GRIB files.
for grib_file in grib_file_list:
    print("\nReading data file:", grib_file)

    dataset = xr.open_dataset(grib_file, engine="cfgrib")

    for data_var in DATA_VARS:
        # Check if data variable is found in dataset.
        if data_var not in dataset.variables:
            print(f"Variable {data_var} not found in {grib_file}")
            continue

        for i, date_stamp in enumerate(dataset["time"]):
            if i == 0:
                # Skip start date which is usually full of NaNs.
                continue

            date_val = pd.to_datetime(date_stamp.values)
            year = date_val.year
            month = date_val.month
            day = date_val.day
            date_str = f"{year}-{month:02}-{day:02}"

            #  Select data variable slice for current date stamp.
            data_array = dataset[data_var][i]

            # Data upsampling
            if SCALE_FACTOR <= 1:
                # Skip upsampling if scale factor is less than unity.
                continue
            data_array = upsample_data(data_array, SCALE_FACTOR, SCALE_FACTOR)
            print(f"Variable {data_var}, {date_str}: Upsampling completed.")

            # Mask data outside Uttarakhand shapefile boundaries.
            data_array = data_array.where(shp_mask)

            # Data aggregation via min, max, and sum (if applicable)
            if data_var in ACCUMULATED_VARS:
                # Data variable value at step 1 = Value at step 1
                step_1 = data_array[[0]]
                # Compute first-order differences to obtain values at steps > 1.
                steps_gtr_1 = data_array.diff(dim="step")
                # Concatenate data values at different steps.
                data_array = xr.concat([step_1, steps_gtr_1], dim="step")
                # Drop incomplete last hour if final day of dataset is reached.
                if i == len(dataset["time"]) - 1:
                    data_array = data_array[:-1]
                if data_var == "tp":
                    # Set negative values arising from numerical instability to zero.
                    data_array = data_array.where(
                        (data_array > 0) | data_array.isnull(), 0
                    )

            # Minimum value of data variable over hourly measurements
            min_data_var_array = data_array.min(dim="step")
            max_data_var_array = data_array.max(dim="step")

            # Create a new output directory for every (data_var_min, year, month) tuple.
            minvar_outpath = (
                OUTPUT_PATH / (data_var + "_min") / str(year) / f"{month:02d}"
            )
            if not os.path.isdir(minvar_outpath):
                os.makedirs(minvar_outpath)
            # Write minimum hourly data variable raster to disk.
            MIN_OUTFILE = str(
                minvar_outpath / f"{data_var}_min_{year}_{month:02d}_{day:02d}.tif"
            )
            min_data_var_array.rio.to_raster(MIN_OUTFILE, dtype=np.float32)
            print(f"Variable {data_var}_min, {date_str}: GeoTiff file written.")

            # Create a new output directory for every (data_var_max, year, month) tuple.
            maxvar_outpath = (
                OUTPUT_PATH / (data_var + "_max") / str(year) / f"{month:02d}"
            )
            if not os.path.isdir(maxvar_outpath):
                os.makedirs(maxvar_outpath)
            # Write maximum hourly data variable raster to disk.
            MAX_OUTFILE = str(
                maxvar_outpath / f"{data_var}_max_{year}_{month:02d}_{day:02d}.tif"
            )
            max_data_var_array.rio.to_raster(MAX_OUTFILE, dtype=np.float32)
            print(f"Variable {data_var}_max, {date_str}: GeoTiff file written.")

            if data_var in ACCUMULATED_VARS:
                # Summed value of data variable over hours of everyday
                sum_data_var_array = data_array.sum(dim="step", skipna=False)
                if i == len(dataset["time"]) - 1:
                    # Linear scaling to cover for incomplete final hour of last day
                    N_hours = len(data_array["step"])
                    sum_data_var_array *= (N_hours + 1) / N_hours
                sumvar_outpath = (
                    OUTPUT_PATH / (data_var + "_sum") / str(year) / f"{month:02d}"
                )
                # Create a new output directory for every (data_var_sum, year, month) tuple.
                if not os.path.isdir(sumvar_outpath):
                    os.makedirs(sumvar_outpath)
                # Write summed data variable raster to disk.
                SUM_OUTFILE = str(
                    sumvar_outpath / f"{data_var}_sum_{year}_{month:02d}_{day:02d}.tif"
                )
                sum_data_var_array.rio.to_raster(SUM_OUTFILE, dtype=np.float32)
                print(f"Variable {data_var}_sum, {date_str}: GeoTiff file written.")

print("\nProcessing completed.")
end_time = time.time()
run_time_mins = (end_time - start_time) / 60
print(f"Code run time = {run_time_mins: .2f} minutes")
