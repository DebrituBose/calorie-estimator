import streamlit as st
import joblib
import numpy as np

# Custom page config
st.set_page_config(page_title="Calorie Estimator", page_icon="🔥", layout="centered")

# --- Sidebar ---
st.sidebar.title("📊 Project Info")
st.sidebar.info("""
**Fitness Activity Calorie Estimator**  
Predict calories burned based on workout type, weight, and duration.

👤 **Made by:** Debritu Bose, Sudipta Halder, Antarika Banerjee, Roopsha  
📅 **Date:** July 2025  
""")

# --- Main Title ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🔥 Fitness Calorie Estimator 🔥</h1>", unsafe_allow_html=True)
st.write("Estimate calories burned based on your workout details.")

# --- Load model ---
try:
    model = joblib.load('calorie_model.pkl')
    st.success("✅ Model Loaded Successfully!")
except Exception as e:
    st.error(f"❌ Model Load Error: {e}")

# --- User Inputs ---
st.markdown("---")
st.header("🏋️‍♂️ Enter Workout Details")

workout_types = {
    'Cardio': 0,
    'Strength Training': 1,
    'Yoga': 2,
    'HIIT': 3
}

col1, col2 = st.columns(2)
with col1:
    workout = st.selectbox("Workout Type", list(workout_types.keys()))
with col2:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)

duration = st.slider("Session Duration (hours)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

# --- Prediction ---
st.markdown("---")
if st.button("Estimate Calories Burned 🔍"):
    input_data = np.array([[workout_types[workout], weight, duration]])
    try:
        calories = model.predict(input_data)[0]
        st.success(f"🔥 You burned approximately **{calories:.2f} kcal**!")
    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
