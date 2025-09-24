import streamlit as st
import pandas as pd
import datetime

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Water Intake Tracker 💧", layout="centered")

st.title("💧 Water Intake Tracker")
st.write("Track your daily hydration and reach your water goals!")

# ---------------- Session State ----------------
if "water_log" not in st.session_state:
    st.session_state.water_log = pd.DataFrame(columns=["Date", "Intake (L)"])

# ---------------- Inputs ----------------
goal = st.number_input("Daily Goal (Liters)", min_value=1.0, max_value=10.0, value=3.0, step=0.5)

date = st.date_input("Select Date", value=datetime.date.today())
intake = st.number_input("Water Intake (Liters)", min_value=0.0, step=0.1)

if st.button("Add Entry"):
    new_entry = pd.DataFrame({"Date": [date], "Intake (L)": [intake]})
    st.session_state.water_log = pd.concat([st.session_state.water_log, new_entry], ignore_index=True)
    st.success(f"✅ Added {intake} L on {date}")

# ---------------- Progress Tracker ----------------
today = datetime.date.today()
today_data = st.session_state.water_log[st.session_state.water_log["Date"] == today]

if not today_data.empty:
    total_today = today_data["Intake (L)"].sum()
else:
    total_today = 0.0

progress = min(total_today / goal, 1.0)

st.subheader("Today's Progress")
st.progress(progress)
st.info(f"💧 {total_today:.2f} L / {goal:.2f} L")

# ---------------- Weekly Chart ----------------
st.subheader("📊 Weekly Hydration Chart")

# Get last 7 days
start_date = today - datetime.timedelta(days=6)
weekly_data = st.session_state.water_log[
    (st.session_state.water_log["Date"] >= start_date) & 
    (st.session_state.water_log["Date"] <= today)
]

if not weekly_data.empty:
    weekly_summary = weekly_data.groupby("Date")["Intake (L)"].sum().reset_index()
    st.bar_chart(weekly_summary.set_index("Date"))
else:
    st.warning("No water intake data for the past week.")

# ---------------- Show Full Log ----------------
st.subheader("📒 Full Log")
st.dataframe(st.session_state.water_log.sort_values("Date"))
