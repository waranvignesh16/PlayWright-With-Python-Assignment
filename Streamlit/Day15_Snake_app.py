import streamlit as st
import random
import time

# -----------------------
# Initialize Session State
# -----------------------
BOARD_WIDTH = 40   # 40 columns
BOARD_HEIGHT = 10  # 10 rows

if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5)]  # starting position
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1))
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.start_time = time.time()  # track play time

# -----------------------
# Helper Functions
# -----------------------
def new_food():
    """Generate new food position not overlapping with snake."""
    while True:
        pos = (random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1))
        if pos not in st.session_state.snake:
            return pos

def move_snake():
    """Move snake in current direction."""
    if st.session_state.game_over:
        return

    head_x, head_y = st.session_state.snake[0]

    if st.session_state.direction == "UP":
        head_y -= 1
    elif st.session_state.direction == "DOWN":
        head_y += 1
    elif st.session_state.direction == "LEFT":
        head_x -= 1
    elif st.session_state.direction == "RIGHT":
        head_x += 1

    new_head = (head_x, head_y)

    # Check collision (walls or self)
    if (
        head_x < 0 or head_x >= BOARD_WIDTH or head_y < 0 or head_y >= BOARD_HEIGHT
        or new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        return

    # Insert new head
    st.session_state.snake.insert(0, new_head)

    # Check food
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = new_food()
    else:
        st.session_state.snake.pop()

def reset_game():
    st.session_state.snake = [(5, 5)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1))
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.start_time = time.time()

# -----------------------
# UI Controls
# -----------------------
st.title("🐍 Snake Game (10 × 40 Grid)")

# -----------------------
# Compact Arrow Buttons (Joystick style)
# -----------------------
# Up arrow row
col1, col2, col3 = st.columns([1, 1, 1])
with col1: st.write("")  # empty
with col2:
    if st.button("⬆️") and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
with col3: st.write("")  # empty

# Left, Down, Right row
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⬅️") and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
with col2:
    if st.button("⬇️") and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
with col3:
    if st.button("➡️") and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"

# Restart button
if st.button("🔄 Restart"):
    reset_game()
    st.rerun()

# -----------------------
# Render Game Board
# -----------------------
board = [["⬜" for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# Place snake
for i, (x, y) in enumerate(st.session_state.snake):
    board[y][x] = "🟦" if i == 0 else "🟩"  # Head = 🟦, Body = 🟩

# Place food
fx, fy = st.session_state.food
board[fy][fx] = "🍎"

# Display board
for row in board:
    st.text("".join(row))

# -----------------------
# Display Score
# -----------------------
st.write(f"**Current Score:** {st.session_state.score}")

# -----------------------
# Game Loop (Auto refresh)
# -----------------------
if not st.session_state.game_over:
    move_snake()
    time.sleep(0.2)  # snake speed
    st.rerun()
else:
    st.error("💀 Game Over!")
    play_time = int(time.time() - st.session_state.start_time)
    st.subheader("📊 Final Game Stats")
    st.write(f"✅ **Score:** {st.session_state.score}")
    st.write(f"🍎 **Food Eaten:** {st.session_state.score}")
    st.write(f"🐍 **Snake Length:** {len(st.session_state.snake)}")
    st.write(f"⏱ **Play Time:** {play_time} seconds")
