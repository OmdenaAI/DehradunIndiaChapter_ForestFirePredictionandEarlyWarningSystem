import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def fetch_fire_data(api_key, shapefile_path, days): 
    """
    Fetches fire data from the FIRMS API, filters it based on a specific region, and returns 
    the filtered data as a GeoDataFrame.

    Parameters:
        api_key (str): 
            The API key for accessing the FIRMS data. You can get this from the FIRMS website.
        
        shapefile_path (str): 
            The file path to the shapefile that defines the region of interest. 
            The shapefile must be in a valid format (e.g., .shp).
        
        days (int, optional): 
            The number of days of fire data to fetch. Defaults to 1. 
            It is used to filter the fire data based on the number of past days.
            The API will fetch data for the given number of recent days.

    Returns:
        geopandas.GeoDataFrame: 
            A GeoDataFrame containing the filtered fire data points within the specified region. 
            The data includes columns for latitude, longitude, and other fire-related metrics (e.g., brightness).

    Raises:
        Exception: 
            If there is an error in fetching or processing the data, an exception is raised.
        
        ValueError: 
            If the data from the FIRMS API is missing required columns (e.g., 'longitude' or 'latitude').

    Example:
        # Example usage of the function:
        api_key = 'your_api_key_here'
        shapefile_path = 'path_to_shapefile.shp'
        fire_data = fetch_fire_data(api_key, shapefile_path, days=3)
        print(fire_data.head())
    """
    try:
        # Define the URL for the FIRMS API to fetch fire data for the given number of days
        area_url = f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/{api_key}/VIIRS_SNPP_NRT/IND/{days}'
        
        # Fetch the fire data from the API
        df_area = pd.read_csv(area_url)
        
        # Check if the required columns ('longitude' and 'latitude') exist in the data
        if 'longitude' not in df_area.columns or 'latitude' not in df_area.columns:
            raise ValueError("FIRMS data must contain 'longitude' and 'latitude' columns.")

        # Load the shapefile that defines the region of interest
        region_shape = gpd.read_file(shapefile_path)
        
        # Ensure the shapefile is in the WGS 84 CRS (EPSG:4326)
        region_shape.crs = "EPSG:4326"
        region_shape = region_shape.to_crs("EPSG:4326")  # Reproject to EPSG:4326 if necessary
        
        # Convert the FIRMS data (latitude, longitude) to a GeoDataFrame
        gdf_area = gpd.GeoDataFrame(
            df_area,
            geometry=[Point(xy) for xy in zip(df_area['longitude'], df_area['latitude'])],
            crs="EPSG:4326"
        )

        # Filter the fire data points that lie within the region defined by the shapefile
        gdf_filtered = gdf_area[gdf_area.geometry.within(region_shape.geometry.union_all())]
        
        # Return the filtered GeoDataFrame
        return gdf_filtered

    except Exception as e:
        raise Exception(f"An error occurred while fetching fire data: {str(e)}")