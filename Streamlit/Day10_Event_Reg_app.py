import streamlit as st
import pandas as pd

# ----------------- Page Setup -----------------
st.set_page_config(page_title="🎉 Event Registration", layout="centered")
st.title("🎉 Event Registration System")

# ----------------- Session State Init -----------------
if "registrations" not in st.session_state:
    st.session_state["registrations"] = []

# ----------------- Registration Form -----------------
with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    event_choice = st.selectbox("Select Event", ["Hackathon", "Workshop", "Seminar", "Networking"])

    submitted = st.form_submit_button("Register ✅")

    if submitted:
        if name and email:
            st.session_state["registrations"].append(
                {"Name": name, "Email": email, "Event": event_choice}
            )
            st.success(f"Thanks {name}! You are registered for {event_choice}.")
        else:
            st.error("⚠️ Please fill in all fields before submitting.")

# ----------------- Show Live Stats -----------------
st.subheader("📊 Registration Summary")

total_regs = len(st.session_state["registrations"])
st.metric("Total Registrations", total_regs)

if total_regs > 0:
    df = pd.DataFrame(st.session_state["registrations"])
    st.dataframe(df, use_container_width=True)

    # ----------------- Export Option -----------------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Registrations as CSV",
        data=csv,
        file_name="event_registrations.csv",
        mime="text/csv",
    )
