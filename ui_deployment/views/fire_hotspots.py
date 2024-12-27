import json
import pandas as pd
import folium
import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
from streamlit_folium import st_folium
from utils.fetch_fire_data import fetch_fire_data

# Streamlit App
st.subheader("Latest Wildfire Hot-spots Around Uttarakhand State")

# Add a button to refresh data manually
if st.button("Refresh Data"):
    st.cache_data.clear()  # Clear the cache to fetch fresh data

# Dropdown for selecting the filter
date_filter = st.selectbox(
    "Select Day Range:",
    ["Today", "Last 2 Days", "Last 3 Days"]
)

# Set the number of days based on the selected filter
if date_filter == "Today":
    DAYS = 1
elif date_filter == "Last 2 Days":
    DAYS = 2
elif date_filter == "Last 3 Days":
    DAYS = 3

# Fetch wildfire data with caching
@st.cache_data(ttl=3600)  # Cache for 1 hour (3600 seconds)
def get_cached_fire_data(api_key, shapefile_path, days):
    try:
        # Fetch the wildfire data
        fire_data = fetch_fire_data(api_key, shapefile_path, days)
        return fire_data
    except Exception as e:
        st.error(f"An error occurred while fetching wildfire data: {str(e)}")
        return pd.DataFrame()

# Get the current directory dynamically
base_dir = Path(__file__).resolve().parent

# Define the path to the GeoJSON file in the assets folder
geojson_file_path = base_dir.parent / 'assets' / 'uttarakhand.geojson'

MAP_KEY = st.secrets["MAP_KEY"]
shap_file_path = base_dir.parent / 'assets' / 'uttarakhand_WGS1984.shp'

# Fetch the data based on the selected date range
fire_data = get_cached_fire_data(MAP_KEY, shap_file_path, DAYS)

# Read the GeoJSON file
with open(geojson_file_path, 'r') as file:
    uttarakhand_boundary = json.load(file)

# Create a map centered around Dehradun (Uttarakhand's capital)
m = folium.Map(location=[30.3756, 79.3493], zoom_start=9)

# Add the boundary of Uttarakhand using GeoJSON
folium.GeoJson(
    uttarakhand_boundary,
    name="Uttarakhand Boundary",
    style_function=lambda x: {
        'fillColor': 'blue',
        'color': 'blue',
        'weight': 2,
        'fillOpacity': 0
    }
).add_to(m)

# Add Uttarakhand's capital marker
STATE_DATA = {'capital': 'Dehradun', 'latitude': 30.3165, 'longitude': 78.0322}
folium.Marker(
    location=[STATE_DATA['latitude'], STATE_DATA['longitude']],
    popup=f"{STATE_DATA['capital']}, Uttarakhand",
    tooltip=f"{STATE_DATA['capital']}, Uttarakhand",
    icon=folium.Icon(color="blue")
).add_to(m)

# Filter the fire data based on the selected date range
if not fire_data.empty:
    fire_data['acq_date'] = pd.to_datetime(fire_data['acq_date'], format='%Y-%m-%d')

    # Add wildfire markers for the filtered data
    for _, fire in fire_data.iterrows():
        # Convert acquisition time to 24-hour format
        acq_time = str(fire['acq_time']).zfill(4)  # Ensure it's 4 digits (e.g., "0033")
        formatted_time = f"{acq_time[:2]}:{acq_time[2:]}"  # Format as HH:MM

        # Add CircleMarker for each wildfire
        folium.CircleMarker(
            location=[fire['latitude'], fire['longitude']],
            radius=5,
            popup=(
                f"Latitude: {fire['latitude']}<br>"
                f"Longitude: {fire['longitude']}<br>"
                f"Brightness: {fire['bright_ti4']}<br>"
                f"Date: {fire['acq_date']}<br>"
                f"Time: {formatted_time} UTC<br>"  # Use formatted 24-hour time
                f"Daynight: {fire['daynight']}"
            ),
            color="red",
            fill=True,
            fill_color="red"
        ).add_to(m)
else:
    st.warning("No wildfire data available for Uttarakhand.")

# Display the map in Streamlit
st_folium(
    m,
    width=1200,
    height=500,
)
