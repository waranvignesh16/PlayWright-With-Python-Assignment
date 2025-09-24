import streamlit as st

st.title("🧮 Simple Calculator")

# Session state to keep history
if "history" not in st.session_state:
    st.session_state.history = []

# Inputs
num1 = st.number_input("Enter first number:", value=0.0, step=1.0)
num2 = st.number_input("Enter second number:", value=0.0, step=1.0)
operation = st.selectbox("Select operation:", ["➕ Add", "➖ Subtract", "✖️ Multiply", "➗ Divide"])

# Calculate button
if st.button("Calculate"):
    result = None
    if operation == "➕ Add":
        result = num1 + num2
    elif operation == "➖ Subtract":
        result = num1 - num2
    elif operation == "✖️ Multiply":
        result = num1 * num2
    elif operation == "➗ Divide":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("Division by zero is not allowed!")

    if result is not None:
        st.success(f"Result: {result}")
        # Save to history
        st.session_state.history.append(f"{num1} {operation[0]} {num2} = {result}")

# Show history
if st.session_state.history:
    st.subheader("📜 Calculation History")
    for calc in st.session_state.history[::-1]:  # show latest first
        st.write(calc)
