import streamlit as st
import pandas as pd
import datetime

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Gym Workout Logger 🏋️", layout="centered")

st.title("🏋️ Gym Workout Logger")
st.write("Log your workouts and track progress over time!")

# ---------------- Session State ----------------
if "workouts" not in st.session_state:
    st.session_state.workouts = pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight (kg)", "Total Volume"])

# ---------------- Exercise List ----------------
exercise_list = [
    "Bench Press", "Incline Bench Press", "Chest Fly",
    "Squat", "Leg Press", "Lunges", "Deadlift",
    "Pull Ups", "Lat Pulldown", "Barbell Row",
    "Bicep Curl", "Tricep Extension", "Shoulder Press",
    "Lateral Raises", "Plank", "Crunches"
]

# ---------------- Input Form ----------------
with st.form("workout_form"):
    date = st.date_input("Workout Date", value=datetime.date.today())
    exercise = st.selectbox("Exercise", exercise_list)
    sets = st.number_input("Sets", min_value=1, value=3, step=1)
    reps = st.number_input("Reps per Set", min_value=1, value=10, step=1)
    weight = st.number_input("Weight per Rep (kg)", min_value=0.0, value=20.0, step=2.5)

    submitted = st.form_submit_button("Add Workout")

    if submitted:
        total_volume = sets * reps * weight
        new_entry = pd.DataFrame({
            "Date": [date],
            "Exercise": [exercise],
            "Sets": [sets],
            "Reps": [reps],
            "Weight (kg)": [weight],
            "Total Volume": [total_volume]
        })
        st.session_state.workouts = pd.concat([st.session_state.workouts, new_entry], ignore_index=True)
        st.success(f"✅ Logged {exercise} ({sets}x{reps} @ {weight}kg) on {date}")

# ---------------- Workout History ----------------
st.subheader("📒 Workout History")
if not st.session_state.workouts.empty:
    st.dataframe(st.session_state.workouts.sort_values("Date", ascending=False))
else:
    st.warning("No workouts logged yet.")

# ---------------- Weekly Progress ----------------
st.subheader("📊 Weekly Progress")

if not st.session_state.workouts.empty:
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=6)
    
    weekly_data = st.session_state.workouts[
        (st.session_state.workouts["Date"] >= start_date) &
        (st.session_state.workouts["Date"] <= today)
    ]

    if not weekly_data.empty:
        summary = weekly_data.groupby("Date")["Total Volume"].sum().reset_index()
        st.bar_chart(summary.set_index("Date"))
    else:
        st.info("No workouts logged in the past week.")
