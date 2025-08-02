import streamlit as st
import joblib
import numpy as np
import pandas as pd
import io

st.set_page_config(page_title="Calorie Estimator", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #ffe4c4, #fffdd0);
    }
    .main {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 30px;
        margin: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #FF4B4B;
    }
    .stButton>button {
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #feb47b, #ff7e5f);
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: linear-gradient(to right, #FF4B4B, #e63946);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("📊 Project Info")
st.sidebar.info("""
**Fitness Calorie Estimator**  
🔍 Predict calories burned per workout.

👤 **By:** Debritu Bose, Sudipta Halder, Antarika Banerjee, Roopsha 
📅 July 2025
""")

st.markdown("<h1 style='text-align:center;'>🔥 Calorie Burn Estimator 🔥</h1>", unsafe_allow_html=True)
st.write("Estimate calories burned based on workout type, your weight, and session duration.")

try:
    model = joblib.load('calorie_model.pkl')
except Exception as e:
    st.error(f"❌ Model Load Error: {e}")

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

if st.button("🔥 Estimate Calories Burned"):
    try:
        input_df = pd.DataFrame(
            [[workout_types[workout], weight, duration]],
            columns=['Workout_Type', 'Weight (kg)', 'Session_Duration (hours)']
        )
        calories = model.predict(input_df)[0]

        st.markdown(f"""
            <div style="background-color:#f0fff0; padding:15px; border-radius:10px; border:1px solid #28a745;">
            <h2 style="color:#28a745;">🔥 Estimated Calories Burned: {calories:.2f} kcal</h2>
            </div>
        """, unsafe_allow_html=True)

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

st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit | © Debritu Bose, Sudipta Halder, Antarika Banerjee, Roopsha
</div>
""", unsafe_allow_html=True)

