import streamlit as st

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Currency Converter 💱", layout="centered")

st.title("💱 Currency Converter")
st.write("Convert between INR, USD, EUR, etc. using static rates.")

# ---------------- Static Conversion Rates ----------------
# Base currency: 1 USD
exchange_rates = {
    "USD": 1.0,
    "INR": 83.0,   # 1 USD = 83 INR
    "EUR": 0.92,   # 1 USD = 0.92 EUR
    "GBP": 0.79,   # 1 USD = 0.79 GBP
    "JPY": 148.0,  # 1 USD = 148 JPY
    "AUD": 1.55    # 1 USD = 1.55 AUD
}

currencies = list(exchange_rates.keys())

# ---------------- Inputs ----------------
col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("From Currency", currencies, index=1)  # Default INR
    amount = st.number_input("Enter Amount", min_value=0.0, value=100.0, step=1.0)

with col2:
    to_currency = st.selectbox("To Currency", currencies, index=0)  # Default USD

# ---------------- Conversion ----------------
if st.button("Convert"):
    # Convert to USD first
    amount_in_usd = amount / exchange_rates[from_currency]
    # Then convert to target currency
    converted_amount = amount_in_usd * exchange_rates[to_currency]

    st.success(f"💹 {amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")
