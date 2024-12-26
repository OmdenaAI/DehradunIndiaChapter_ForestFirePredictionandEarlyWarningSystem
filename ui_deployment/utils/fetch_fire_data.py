import pandas as pd
import streamlit as st

# Function to fetch wildfire data
def fetch_wildfire_data(lat_min, lat_max, lon_min, lon_max):
    """
    Fetch wildfire data from the API and filter it for Uttarakhand.
    
    Args:
        map_key (str): The API key for the data source.
        lat_min, lat_max (float): Latitude bounds for Uttarakhand.
        lon_min, lon_max (float): Longitude bounds for Uttarakhand.
        
    Returns:
        pd.DataFrame: Filtered wildfire data.
    """
    try:
        map_key = st.secrets["MAP_KEY"]
        area_url = f'https://firms.modaps.eosdis.nasa.gov/api/area/csv/{map_key}/VIIRS_SNPP_NRT/world/1'
        df_area = pd.read_csv(area_url)
        df_filtered = df_area[
            (df_area['latitude'] >= lat_min) & (df_area['latitude'] <= lat_max) &
            (df_area['longitude'] >= lon_min) & (df_area['longitude'] <= lon_max)
        ]
        return df_filtered
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()