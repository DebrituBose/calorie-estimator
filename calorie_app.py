import streamlit as st
import joblib
import numpy as np
import pandas as pd
import io

# Page config
st.set_page_config(page_title="Calorie Estimator", page_icon="🔥", layout="wide")

# --- Custom CSS with Background Color ---
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
    }
    .main {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin: 20px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #e63946;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: linear-gradient(to right, #FF4B4B, #e63946);
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Info ---
st.sidebar.title("📊 Project Info")
st.sidebar.info("""
**Fitness Calorie Estimator**  
🔍 Predict calories burned per workout.

👤 **By:** Debritu Bose  
📅 August 2025
""")

# --- Title ---
st.markdown("<h1 style='text-align:center; color:#FF4B4B;'>🔥 Calorie Burn Estimator 🔥</h1>", unsafe_allow_html=True)
st.write("Estimate calories burned based on workout type, your weight, and session duration.")

# --- Load Model ---
try:
    model = joblib.load('calorie_model.pkl')
except Exception as e:
    st.error(f"❌ Model Load Error: {e}")

# --- Inputs ---
st.markdown("### 🏋️ Workout Details")
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
    weight = st.slider("Weight (kg)", 30.0, 200.0, 70.0)

duration = st.slider("Session Duration (hours)", 0.1, 5.0, 1.0, step=0.1)

st.markdown("---")

# --- Prediction Using Correct Column Names ---
if st.button("🔥 Estimate Calories Burned"):
    try:
        # Match column names to training data
        input_df = pd.DataFrame(
            [[workout_types[workout], weight, duration]],
            columns=['Workout_Type', 'Weight (kg)', 'Session_Duration (hours)']
        )
        calories = model.predict(input_df)[0]

        st.markdown(f"""
            <div style="background-color:#d9f9d9; padding:15px; border-radius:10px;">
            <h2 style="color:#28a745;">🔥 Estimated Calories Burned: {calories:.2f} kcal</h2>
            </div>
        """, unsafe_allow_html=True)

        # --- Chart ---
        st.markdown("### 📊 Estimated Calories Comparison")
        chart_data = {
            'Workout Type': ['Cardio', 'Strength', 'Yoga', 'HIIT'],
            'Calories Burned': [
                calories + 50,
                calories + 30,
                calories - 20,
                calories + 70
            ]
        }
        df_chart = pd.DataFrame(chart_data)
        st.bar_chart(df_chart.set_index('Workout Type'))

        # --- Download Report ---
        st.markdown("### 📥 Download Your Report")
        report = f"""
Workout: {workout}
Weight: {weight} kg
Duration: {duration} hrs
Calories Burned: {calories:.2f} kcal
"""
        st.download_button("Download Result", report, file_name="calorie_report.txt")

    except Exception as e:
        st.error(f"Prediction failed: {e}")

# --- Footer ---
st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit | © Debritu Bose
</div>
""", unsafe_allow_html=True)
