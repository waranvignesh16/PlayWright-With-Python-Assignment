import streamlit as st

st.title("My First Streamlit app")

name = st.text_input("Enter Your Name")

if st.button("Say Hello"):
    if name:
        st.success(f"hello {name}, Welcome to my page")
    else:
        st.warning("Please enter your name")