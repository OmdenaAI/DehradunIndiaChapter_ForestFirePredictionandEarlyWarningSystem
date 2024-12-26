import streamlit as st


# --- PAGE SETUP ---
home_page = st.Page(
    "views/home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)
wildfire_analysis_page = st.Page(
    "views/wildfire_analysis.py",
    title="Wildfire Analysis",
    icon="🔥",
)
fire_hotspots_page = st.Page(
    "views/fire_hotspots.py",
    title="Fire Hotspots",
    icon="🛰️",
)
dataset_visualization = st.Page(
    "views/dataset_visualization.py",
    title="Dataset Visualization",
    icon="📊",
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [home_page],
        "Analysis": [wildfire_analysis_page, fire_hotspots_page, dataset_visualization],
    }
)

# --- SHARED ON ALL PAGES ---
st.logo("assets/omdena_dehradun_chapter_logo.jpeg", size="large")
st.sidebar.image("assets/omdena_logo.png")
st.sidebar.markdown("Made with ❤️ by Omdena Community")


# --- RUN NAVIGATION ---
pg.run()
