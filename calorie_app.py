import streamlit as st
import joblib
import numpy as np
import pandas as pd
import io


st.set_page_config(page_title="Calorie Estimator", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    body {
        background-image: url(https://images.unsplash.com/photo-1558611848-73f7eb4001a1?auto=format&fit=crop&w=1920&q=80
)
);
        background-size: cover;
        background-attachment: fixed;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.88);
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

st.sidebar.title("📊 Project Info")
st.sidebar.info("""
**Fitness Calorie Estimator**  
🔍 Predict calories burned per workout.

👤 **By:** Debritu Bose, Sudipta Halder, Antarika Banerjee, Roopsha 
📅 july 2025  
""")
st.image("https://cdn.pixabay.com/photo/2017/04/30/11/54/dumbbell-2278889_1280.png", width=150)

st.markdown("<h1 style='text-align:center; color:#FF4B4B;'>🔥 Calorie Burn Estimator 🔥</h1>", unsafe_allow_html=True)
st.write("Estimate calories burned based on workout type, your weight, and session duration.")

try:
    model = joblib.load('calorie_model.pkl')
    st.success("✅ Model loaded successfully!")
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
    input_data = np.array([[workout_types[workout], weight, duration]])
    try:
        calories = model.predict(input_data)[0]
        st.markdown(f"""
            <div style="background-color:#d9f9d9; padding:15px; border-radius:10px;">
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

