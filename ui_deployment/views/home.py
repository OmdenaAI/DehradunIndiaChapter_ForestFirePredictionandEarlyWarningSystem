import streamlit as st

from forms.contact import contact_form


@st.experimental_dialog("Contact Me")
def show_contact_form():
    contact_form()


# --- MAIN TITLE ---
st.title("Omdena Dehradun Chapter", anchor=False)

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/omdena_dehradun_chapter_logo.jpeg", width=230)

with col2:
    st.subheader("Protect Uttarakhand's Forests with AI 🌳🔥", anchor=False)
    st.write(
        """
        Welcome to the Dehradun Chapter of Omdena, where we leverage AI to protect 
        the forests of Uttarakhand from wildfires and environmental degradation. 🌲🔥 Join us in making a difference with cutting-edge technology and teamwork.
        """
    )
    if st.button("✉️ Contact Us"):
        show_contact_form()


# ---Why Join?-------------------------------------------
st.write("\n")
st.subheader("Why Join ?", anchor=False)
st.write(
    """
    - Make a Difference: Help protect Uttarakhand's beautiful forests 🌲
    - Learn New Skills: Gain expertise in ML, CV, GIS, and more 💻
    - Collaborate Globally: Work with talented individuals from around the world 🌍
    """
)

# --- What We Need ---
st.write("\n")
st.subheader("What We Need", anchor=False)
st.write(
    """
    - Machine Learning Experts 🧠
    - Computer Vision Enthusiasts 👀
    - Data Analysts 📊
    - GIS Specialists 🗺️
    - Environmental Conservationists 🌱
    """
)
