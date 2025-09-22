import streamlit as st
import requests
import pandas as pd

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Unit Converter 🔄", layout="centered")

# ---------------- Dark/Light Mode ----------------
dark_mode = st.sidebar.checkbox("Dark Mode 🌙", value=False)

if dark_mode:
    bg_color = "#181818"
    text_color = "#FFFFFF"
    box_color = "#282828"
else:
    bg_color = "#F0F0F0"
    text_color = "#000000"
    box_color = "#ffffffcc"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg_color};
    color: {text_color};
}}
.converter-box {{
    background-color: {box_color};
    padding: 1.5rem 2rem;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}}
</style>
""", unsafe_allow_html=True)

st.title("Unit Converter 🔄")
st.write("Convert Currency, Temperature, Length, and Weight instantly.")

# ---------------- Tabs ----------------
tab1, tab2, tab3, tab4 = st.tabs(["💱 Currency", "🌡️ Temperature", "📏 Length", "⚖️ Weight"])

# ---------------- Currency Converter ----------------
with tab1:
    st.subheader("💱 Currency Converter")
    swap = st.checkbox("Swap Units", key="currency_swap")
    currencies = ["USD", "EUR", "INR", "GBP", "JPY", "AUD", "CAD"]

    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox("From", currencies, index=0)
    with col2:
        to_currency = st.selectbox("To", currencies, index=1)

    if swap:
        from_currency, to_currency = to_currency, from_currency

    amount = st.number_input(f"Amount ({from_currency})", value=1.0, min_value=0.0)

    # ---------------- Fetch Exchange Rate ----------------
    @st.cache_data(ttl=3600)
    def get_conversion(from_curr, to_curr, amt):
        try:
            # Using free API: exchangerate-api.com
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if "rates" in data and to_curr in data["rates"]:
                rate = data["rates"][to_curr]
                return round(rate * amt, 4)
            else:
                st.warning(f"API returned unexpected response: {data}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to currency API: {e}")
            return None

    result = get_conversion(from_currency, to_currency, amount)
    if result is not None:
        st.success(f"{amount} {from_currency} = {result} {to_currency}")
    else:
        st.error("❌ Unable to fetch conversion. Please try again later.")

# ---------------- Temperature ----------------
with tab2:
    st.subheader("🌡️ Temperature Converter")
    swap = st.checkbox("Swap Units", key="temp_swap")
    units = ["Celsius", "Fahrenheit", "Kelvin"]

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From", units)
    with col2:
        to_unit = st.selectbox("To", units)

    if swap:
        from_unit, to_unit = to_unit, from_unit

    temp = st.number_input(f"Temperature ({from_unit})", value=0.0)

    def convert_temp(value, from_u, to_u):
        if from_u == to_u:
            return value
        if from_u == "Celsius":
            if to_u == "Fahrenheit":
                return value*9/5 + 32
            elif to_u == "Kelvin":
                return value + 273.15
        elif from_u == "Fahrenheit":
            if to_u == "Celsius":
                return (value-32)*5/9
            elif to_u == "Kelvin":
                return (value-32)*5/9 + 273.15
        elif from_u == "Kelvin":
            if to_u == "Celsius":
                return value - 273.15
            elif to_u == "Fahrenheit":
                return (value-273.15)*9/5 + 32

    st.success(f"{temp} {from_unit} = {round(convert_temp(temp, from_unit, to_unit),2)} {to_unit}")

# ---------------- Length ----------------
with tab3:
    st.subheader("📏 Length Converter")
    swap = st.checkbox("Swap Units", key="len_swap")
    units = ["Meters", "Kilometers", "Miles", "Feet", "Inches"]
    factors = {"Meters":1,"Kilometers":1000,"Miles":1609.34,"Feet":0.3048,"Inches":0.0254}

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From", units, key="len_from")
    with col2:
        to_unit = st.selectbox("To", units, key="len_to")

    if swap:
        from_unit, to_unit = to_unit, from_unit

    value = st.number_input(f"Value ({from_unit})", value=1.0)
    st.success(f"{value} {from_unit} = {round(value*factors[from_unit]/factors[to_unit],4)} {to_unit}")

# ---------------- Weight ----------------
with tab4:
    st.subheader("⚖️ Weight Converter")
    swap = st.checkbox("Swap Units", key="wt_swap")
    units = ["Kilogram", "Gram", "Pound", "Ounce"]
    factors = {"Kilogram":1,"Gram":0.001,"Pound":0.453592,"Ounce":0.0283495}

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From", units, key="wt_from")
    with col2:
        to_unit = st.selectbox("To", units, key="wt_to")

    if swap:
        from_unit, to_unit = to_unit, from_unit

    value = st.number_input(f"Value ({from_unit})", value=1.0)
    st.success(f"{value} {from_unit} = {round(value*factors[from_unit]/factors[to_unit],4)} {to_unit}")
