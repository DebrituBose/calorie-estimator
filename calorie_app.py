import streamlit as st
import joblib
import numpy as np

st.title("🏋️‍♀️ Fitness Calorie Estimator")
st.write("Estimate calories burned based on your workout details.")

# Safe model load
try:
    model = joblib.load('calorie_model.pkl')
    st.success("✅ Model Loaded Successfully!")
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")

# Workout type options
workout_types = {
    'Cardio': 0,
    'Strength Training': 1,
    'Yoga': 2,
    'HIIT': 3
}

workout = st.selectbox("Workout Type", list(workout_types.keys()))
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
duration = st.number_input("Session Duration (hours)", min_value=0.1, max_value=5.0, value=1.0)

if st.button("Estimate Calories Burned"):
    input_data = np.array([[workout_types[workout], weight, duration]])
    try:
        calories = model.predict(input_data)[0]
        st.success(f"🔥 Estimated Calories Burned: {calories:.2f} kcal")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
