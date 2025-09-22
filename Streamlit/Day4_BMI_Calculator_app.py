import streamlit as st

# 🎨 Page setup
st.set_page_config(page_title="BMI Calculator 🏋️", page_icon="🏋️", layout="centered")

# 🌟 Custom CSS for trendy UI
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 2rem;
        border-radius: 15px;
    }
    .result-box {
        background-color: #ffffffcc;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🏋️ Title
st.title("BMI Calculator 🏋️")

st.write("Enter your height and weight to calculate your **Body Mass Index (BMI)**.")

# 📥 Inputs
col1, col2 = st.columns(2)

with col1:
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)

with col2:
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70)

# 📊 Calculate BMI
if st.button("Calculate BMI"):
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)

    # 🩺 Health category
    if bmi < 18.5:
        category = "Underweight 😟"
        color = "orange"
    elif 18.5 <= bmi < 25:
        category = "Normal ✅"
        color = "green"
    else:
        category = "Overweight ⚠️"
        color = "red"

    # 🎯 Show Result
    st.markdown(
        f"""
        <div class="result-box" style="color:{color};">
            Your BMI is <b>{bmi}</b><br>
            Category: {category}
        </div>
        """,
        unsafe_allow_html=True
    )
