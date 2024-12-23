import json
import folium
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from pathlib import Path

# Title of the app
st.subheader("Real-time Wildfire Hot-spots Around Uttarakhand State")

# Uttarakhand capital data
STATE_DATA = {
    'state': 'Uttarakhand',
    'capital': 'Dehradun',
    'latitude': 30.3165,  # Dehradun Latitude
    'longitude': 78.0322  # Dehradun Longitude
}

# Wildfire occurrence data (expanded example)
FIRE_DATA = pd.DataFrame({
    'latitude': [
        30.45, 30.55, 30.60, 30.35, 30.25, 30.65, 30.75, 30.85, 30.95, 30.15,
        30.05, 30.30, 30.50, 30.70, 30.80
    ],
    'longitude': [
        78.10, 78.20, 78.30, 78.00, 78.10, 78.50, 78.60, 78.70, 78.80, 78.90,
        79.00, 79.10, 79.20, 79.30, 79.40
    ],
})


# Get the current directory dynamically
# Gets the directory of the current script
base_dir = Path(__file__).resolve().parent

# Define the path to the GeoJSON file in the assets folder
geojson_file_path = base_dir.parent / 'assets' / \
    'uttarakhand.geojson'  # Going one step out to 'assets' folder

# Read the GeoJSON file
with open(geojson_file_path, 'r') as file:
    uttarakhand_boundary = json.load(file)

# Create a map centered around Dehradun (Uttarakhand's capital)
m = folium.Map(location=[30.375600469582153, 79.34929469157846], zoom_start=9)

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
folium.Marker(
    location=[STATE_DATA['latitude'], STATE_DATA['longitude']],
    popup=f"{STATE_DATA['capital']}, {STATE_DATA['state']}",
    tooltip=f"{STATE_DATA['capital']}, {STATE_DATA['state']}",
    icon=folium.Icon(color="blue")
).add_to(m)

# Add fire instance markers
for fire in FIRE_DATA.itertuples():
    folium.CircleMarker(
        location=[fire.latitude, fire.longitude],
        radius=10,  # Adjust size based on intensity if desired
        popup=f"Lat:{fire.latitude}<br>Long:{fire.longitude}",
        color="red",
        fill=True,
        fill_color="red"
    ).add_to(m)

# Display the map in Streamlit
st_folium(
    m,
    width=1200,
    height=500,
)
