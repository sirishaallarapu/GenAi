import streamlit as st
import requests

# ✅ Use your ExchangeRate-API Key here
API_KEY = "e0d0dd9f5e0e3c604f02f881"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

st.title("💰 Currency Converter")

# User Inputs
amount = st.number_input("Enter amount:", min_value=0.01, value=1.0, step=0.01)
from_currency = st.text_input("From Currency (e.g., USD):", "USD").upper()
to_currency = st.text_input("To Currency (e.g., INR):", "INR").upper()

# Fetch exchange rates
def convert_currency(amount, from_currency, to_currency):
    url = f"{BASE_URL}{from_currency}"
    response = requests.get(url)

    if response.status_code != 200:
        return "❌ Error fetching exchange rates. Check API key or try again later."
    
    data = response.json()
    
    if "conversion_rates" not in data:
        return "⚠️ Invalid API response. Check API key or base currency."
    
    rates = data["conversion_rates"]
    
    if to_currency not in rates:
        return f"⚠️ Currency {to_currency} not found."
    
    converted_amount = amount * rates[to_currency]
    return f"✅ {amount} {from_currency} = {converted_amount:.2f} {to_currency}"

# Button to trigger conversion
if st.button("Convert"):
    result = convert_currency(amount, from_currency, to_currency)
    st.success(result)
