# tic_tac_toe.py
import streamlit as st
import random

st.set_page_config(page_title="Tic-Tac-Toe ❌⭕", layout="centered")
st.title("Tic-Tac-Toe ❌ ⭕")

# -----------------------
# Helpers
# -----------------------
WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # cols
    (0,4,8), (2,4,6)            # diagonals
]

def check_winner(board):
    """Return (winner, winning_line) where winner is 'X' or 'O' or None"""
    for a,b,c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], (a,b,c)
    if all(board[i] for i in range(9)):
        return "Draw", None
    return None, None

def computer_move_random(board, computer_symbol):
    empties = [i for i,v in enumerate(board) if v == ""]
    if not empties:
        return None
    choice = random.choice(empties)
    board[choice] = computer_symbol
    return choice

def render_static_board_html(board, win_line=None):
    """Return HTML table string to show board with optional highlighted win_line"""
    cell_style = (
        "width:90px;height:90px;display:flex;align-items:center;justify-content:center;"
        "font-size:42px;font-weight:700;border:1px solid #333;border-collapse:collapse;"
    )
    highlight_style = "background:linear-gradient(90deg,#ffe58a,#ffd666);"
    html = "<table style='border-collapse:collapse'>"
    for r in range(3):
        html += "<tr>"
        for c in range(3):
            idx = r*3 + c
            style = cell_style
            if win_line and idx in win_line:
                style += highlight_style
            html += f"<td style='{style}'>{board[idx] if board[idx] else ''}</td>"
        html += "</tr>"
    html += "</table>"
    return html

# -----------------------
# Session state init
# -----------------------
if "board" not in st.session_state:
    st.session_state.board = [""]*9
if "current_player" not in st.session_state:
    st.session_state.current_player = "X"
if "mode" not in st.session_state:
    st.session_state.mode = "2 Players"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "win_line" not in st.session_state:
    st.session_state.win_line = None
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts {"board":..., "winner":..., "by":...}

# -----------------------
# Controls
# -----------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1,1,1])
with col_ctrl1:
    st.session_state.mode = st.selectbox("Mode", ["2 Players", "Vs Computer (Random)"])
with col_ctrl2:
    starter = st.selectbox("Starter", ["X", "O"], index=0)
    # set starting only when new game
with col_ctrl3:
    if st.button("Reset Board"):
        st.session_state.board = [""]*9
        st.session_state.current_player = starter
        st.session_state.winner = None
        st.session_state.win_line = None

# Ensure starter applies when board empty
if all(s == "" for s in st.session_state.board):
    st.session_state.current_player = starter

st.markdown("---")

# -----------------------
# Game grid (interactive)
# -----------------------
st.markdown("### Board")
grid_cols = [st.columns(3) for _ in range(1)]  # just to make layout clear; we will use simple nested loop

# Create 3 rows using columns
for r in range(3):
    cols = st.columns(3)
    for c, col in enumerate(cols):
        idx = r*3 + c
        label = st.session_state.board[idx] if st.session_state.board[idx] else " "
        disabled = (st.session_state.board[idx] != "") or (st.session_state.winner is not None)
        # Key needs to be unique and stable
        if col.button(label, key=f"cell_{idx}", disabled=disabled):
            # if user clicks and cell empty and game not finished
            if st.session_state.board[idx] == "" and st.session_state.winner is None:
                st.session_state.board[idx] = st.session_state.current_player
                # check winner
                w, line = check_winner(st.session_state.board)
                if w:
                    st.session_state.winner = w
                    st.session_state.win_line = line
                    # add to history
                    st.session_state.history.append({
                        "board": st.session_state.board.copy(),
                        "winner": w
                    })
                else:
                    # switch player
                    st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"
                    # if vs computer and it's computer's turn, make a move
                    if st.session_state.mode.startswith("Vs Computer") and st.session_state.current_player == "O":
                        # computer plays 'O' (assuming human is X)
                        computer_move_random(st.session_state.board, "O")
                        w2, line2 = check_winner(st.session_state.board)
                        if w2:
                            st.session_state.winner = w2
                            st.session_state.win_line = line2
                            st.session_state.history.append({
                                "board": st.session_state.board.copy(),
                                "winner": w2
                            })
                        else:
                            st.session_state.current_player = "X"
                # force rerun to refresh UI
                st.rerun()

# -----------------------
# Show status / winning highlight
# -----------------------
st.markdown("---")
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.success("It's a draw!")
    else:
        st.success(f"Winner: {st.session_state.winner}")
    # show highlighted static board
    st.markdown(render_static_board_html(st.session_state.board, st.session_state.win_line), unsafe_allow_html=True)
else:
    st.info(f"Current turn: {st.session_state.current_player}")

# -----------------------
# History & Reset controls
# -----------------------
st.markdown("---")
st.subheader("Match History")
if st.session_state.history:
    for i, rec in enumerate(reversed(st.session_state.history[-20:]), 1):
        winner = rec["winner"]
        board = rec["board"]
        st.markdown(f"**Match {len(st.session_state.history)-i+1}** — Winner: {winner}")
        st.markdown(render_static_board_html(board, None), unsafe_allow_html=True)
else:
    st.write("No finished matches yet.")

# small helper to force reset and start fresh
if st.button("New Game (Clear current)"):
    st.session_state.board = [""]*9
    st.session_state.current_player = starter
    st.session_state.winner = None
    st.session_state.win_line = None
    st.rerun()
