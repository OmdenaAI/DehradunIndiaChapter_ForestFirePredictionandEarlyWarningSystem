import json
import folium
import streamlit as st

from pathlib import Path
from streamlit_folium import st_folium
from utils.fetch_fire_data import fetch_wildfire_data
from datetime import datetime

# Streamlit App
st.subheader("Latest Wildfire Hot-spots Around Uttarakhand State")

# Define constants
LAT_MIN, LAT_MAX = 28.43, 31.27
LON_MIN, LON_MAX = 77.95, 81.02

# Add a button to refresh data manually
if st.button("Refresh Data"):
    st.cache_data.clear()  # Clear the cache to fetch fresh data

# Fetch wildfire data with caching
@st.cache_data(ttl=3600)  # Cache for 1 hour (3600 seconds)
def get_cached_fire_data(lat_min, lat_max, lon_min, lon_max):
    return fetch_wildfire_data(lat_min, lat_max, lon_min, lon_max)

# Fetch the data
fire_data = get_cached_fire_data(LAT_MIN, LAT_MAX, LON_MIN, LON_MAX)

# Get the current directory dynamically
base_dir = Path(__file__).resolve().parent

# Define the path to the GeoJSON file in the assets folder
geojson_file_path = base_dir.parent / 'assets' / 'uttarakhand.geojson'

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

# Add wildfire markers
if not fire_data.empty:
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
