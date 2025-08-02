import streamlit as st
import joblib
import numpy as np


st.set_page_config(page_title="Calorie Estimator", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #f2f2f2;
    }
    .main {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
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

👤 **Made by:** Debritu Bose, Sudipta Halder, Antarika Banerjee, Roopsha 
📅 **July 2025**
""")

with st.container():
    st.markdown("<h1 style='text-align:center; color:#FF4B4B;'>🔥 Calorie Burn Estimator 🔥</h1>", unsafe_allow_html=True)
    st.write("Estimate calories burned based on workout type, your weight, and session duration.")

    try:
        model = joblib.load('calorie_model.pkl')
        st.success("✅ Model loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")

    # Inputs
    workout_types = {
        'Cardio': 0,
        'Strength Training': 1,
        'Yoga': 2,
        'HIIT': 3
    }

    st.markdown("### 🏋️ Workout Details")

    col1, col2 = st.columns(2)
    with col1:
        workout = st.selectbox("Select Workout Type", list(workout_types.keys()))
    with col2:
        weight = st.slider("Your Weight (kg)", 30.0, 200.0, 70.0)

    duration = st.slider("Duration (hours)", 0.1, 5.0, 1.0, step=0.1)

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
        except Exception as e:
            st.error(f"Prediction failed: {e}")

st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit | © Debritu Bose, Sudipta Halder, Antarika Banerjee
</div>
""", unsafe_allow_html=True)
