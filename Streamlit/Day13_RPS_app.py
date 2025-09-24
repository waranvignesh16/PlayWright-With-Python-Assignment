# rps_app.py
import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Rock Paper Scissors ✊🖐️✌️", layout="centered")

# ---- Initialize session state ----
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "comp_score" not in st.session_state:
    st.session_state.comp_score = 0
if "rounds_played" not in st.session_state:
    st.session_state.rounds_played = 0
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {time, user, comp, result}

# ---- Helper logic ----
choices = ["Rock", "Paper", "Scissors"]
emoji = {"Rock":"✊", "Paper":"🖐️", "Scissors":"✌️"}
beats = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper"
}

def play_round(user_choice):
    comp_choice = random.choice(choices)
    if user_choice == comp_choice:
        result = "Draw"
    elif beats[user_choice] == comp_choice:
        result = "You Win"
        st.session_state.user_score += 1
    else:
        result = "Computer Wins"
        st.session_state.comp_score += 1

    st.session_state.rounds_played += 1
    st.session_state.history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": f"{user_choice} {emoji[user_choice]}",
        "computer": f"{comp_choice} {emoji[comp_choice]}",
        "result": result
    })
    return comp_choice, result

def reset_game():
    st.session_state.user_score = 0
    st.session_state.comp_score = 0
    st.session_state.rounds_played = 0
    st.session_state.history = []

# ---- UI ----
st.title("Rock • Paper • Scissors")
st.write("Play against the computer. Keep score and view match history.")

col1, col2 = st.columns([3,1])
with col1:
    mode = st.selectbox("Mode", ["Single Move (press Play)", "First to N Wins"])
with col2:
    if st.button("Reset Game"):
        reset_game()
        st.success("Game reset.")
        st.rerun()

target_wins = None
if mode == "First to N Wins":
    target_wins = st.number_input("Target wins (N)", min_value=1, max_value=50, value=3, step=1)

st.markdown("---")

# Choose move
choice = st.radio("Choose your move:", choices, index=0, horizontal=True)

# Play button
if st.button("Play ▶️"):
    comp_choice, result = play_round(choice)
    st.markdown(f"**You:** {choice} {emoji[choice]}  |  **Computer:** {comp_choice} {emoji[comp_choice]}")
    if result == "Draw":
        st.info("It's a draw!")
    elif result == "You Win":
        st.success("You win this round!")
    else:
        st.error("Computer wins this round!")

# Show scores
st.markdown("### Scoreboard")
col_a, col_b, col_c = st.columns(3)
col_a.metric("Your Score", st.session_state.user_score)
col_b.metric("Computer Score", st.session_state.comp_score)
col_c.metric("Rounds Played", st.session_state.rounds_played)

# Check target win mode
if target_wins:
    if st.session_state.user_score >= target_wins:
        st.balloons()
        st.success(f"You reached {target_wins} wins — You are the champion! 🏆")
    elif st.session_state.comp_score >= target_wins:
        st.error(f"Computer reached {target_wins} wins — Better luck next time!")

st.markdown("---")

# History table (last 10)
st.subheader("Match History (recent first)")
if st.session_state.history:
    hist_df = pd.DataFrame(list(reversed(st.session_state.history[-50:])))
    st.dataframe(hist_df, use_container_width=True)
else:
    st.info("No rounds played yet. Press Play to start!")

st.markdown("---")
st.write("Tips: Use the **First to N Wins** mode for short matches. Click **Reset Game** to clear scores and history.")
