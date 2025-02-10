import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Wildfire Spread Prediction App
st.title("Wildfire Spread Prediction")

# Latitude and Longitude Inputs
st.subheader("Enter the Coordinates of the Area")
latitude = st.number_input("Latitude:", min_value=-90.0, max_value=90.0, step=0.01, format="%.2f")
longitude = st.number_input("Longitude:", min_value=-180.0, max_value=180.0, step=0.01, format="%.2f")

# Submit Button
if st.button("Predict Next Day Wildfire Spread"):
    # Dummy Prediction Logic for demonstration (replace with actual model calls)
    st.write(f"Predicting for location: Latitude {latitude}, Longitude {longitude}")
    
    # Simulate predicted burned mask (replace with real prediction)
    predicted_mask = np.random.random((32, 32))  # Dummy data
    burned_area_km2 = round(np.sum(predicted_mask > 0.5) * 0.01, 2)  # Dummy burned area calculation

    # Simulate fire burning rate (replace with real prediction)
    fire_rate = {
        "North": round(np.random.random() * 10, 2),
        "South": round(np.random.random() * 10, 2),
        "East": round(np.random.random() * 10, 2),
        "West": round(np.random.random() * 10, 2),
    }
    
    # Display Burned Mask
    st.subheader("Predicted Burned Mask")
    fig, ax = plt.subplots()
    ax.imshow(predicted_mask, cmap="hot", interpolation="nearest")
    ax.set_title("Burned Mask Prediction")
    ax.axis("off")
    st.pyplot(fig)
    
    # --- HERO SECTION ---
    col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
    with col1:
        # Display Fire Burning Rate
        st.subheader("Fire Burning Rate (km/h)")
        for direction, rate in fire_rate.items():
            st.write(f"{direction}: {rate} km/h")
    

    with col2:
        # Display Burned Area
        st.subheader("Burned Area")
        st.write(f"Burned Area: {burned_area_km2} km²")
