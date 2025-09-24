import streamlit as st
import time

st.set_page_config(page_title="Stopwatch ⏱", layout="centered")
st.title("⏱ Stopwatch")

# Initialize session state variables
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0
if "history" not in st.session_state:
    st.session_state.history = []

# Format elapsed time
def format_time(elapsed):
    hrs = int(elapsed // 3600)
    mins = int((elapsed % 3600) // 60)
    secs = int(elapsed % 60)
    frac = int((elapsed - int(elapsed)) * 100)  # fastload (hundredths)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}:{frac:02d}"

# Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Start"):
        if not st.session_state.running:
            st.session_state.running = True
            st.session_state.start_time = time.time() - st.session_state.elapsed

with col2:
    if st.button("Stop"):
        if st.session_state.running:
            st.session_state.running = False
            st.session_state.elapsed = time.time() - st.session_state.start_time
            st.session_state.history.append(format_time(st.session_state.elapsed))

with col3:
    if st.button("Reset"):
        st.session_state.running = False
        st.session_state.start_time = 0
        st.session_state.elapsed = 0
        st.session_state.history = []

# Placeholder to update timer in real-time
timer_placeholder = st.empty()

# Update elapsed time if running
if st.session_state.running:
    while st.session_state.running:
        st.session_state.elapsed = time.time() - st.session_state.start_time
        timer_placeholder.markdown(
            f"<h1 style='text-align:center;font-size:70px;font-family:sans-serif'>{format_time(st.session_state.elapsed)}</h1>",
            unsafe_allow_html=True,
        )
        time.sleep(0.05)  # refresh every 50ms
else:
    # Show static timer when not running
    timer_placeholder.markdown(
        f"<h1 style='text-align:center;font-size:70px;font-family:sans-serif'>{format_time(st.session_state.elapsed)}</h1>",
        unsafe_allow_html=True,
    )

# Show Stop history
st.subheader("⏹ Stopwatch History")
if st.session_state.history:
    for i, t in enumerate(reversed(st.session_state.history), 1):
        st.write(f"{i}. {t}")
else:
    st.write("No history yet.")
