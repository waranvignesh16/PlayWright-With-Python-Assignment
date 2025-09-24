import streamlit as st

# Title
st.title("Greeting Form 🎉")

# Input fields
name = st.text_input("Enter your name:")
age = st.slider("Select your age:", 1, 100, 25)

# Show greeting when name is entered
if name:
    st.write(f"Hello, **{name}**! 👋 You are {age} years old.")