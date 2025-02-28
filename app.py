import streamlit as st
import yfinance as yf
from pint import UnitRegistry
from datetime import datetime, timedelta

# Streamlit Page Configuration
st.set_page_config(
    page_title="Unit & Currency Converter",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize unit registry
ureg = UnitRegistry()

# Predefined unit categories with better labels
unit_categories = {
    "📏 Length": ["meter", "kilometer", "mile", "yard", "foot", "inch"],
    "⚖️ Weight": ["gram", "kilogram", "pound", "ounce", "ton"],
    "🌡️ Temperature": ["celsius", "fahrenheit", "kelvin"],
    "🚀 Speed": ["meter/second", "kilometer/hour", "mile/hour", "foot/second"],
    "📦 Volume": ["liter", "milliliter", "gallon", "cubic meter", "cubic foot"]
}

# Currency codes (supported by Yahoo Finance)
currency_codes = ["USD", "EUR", "PKR", "GBP", "JPY", "INR", "CAD", "AUD", "CNY"]

# Function for unit conversion
def convert_units(value, from_unit, to_unit):
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        return result.magnitude
    except Exception as e:
        return f"❌ Error: {e}"

# Function for currency conversion using Yahoo Finance
def convert_currency(amount, from_currency, to_currency):
    try:
        currency_pair = f"{from_currency}{to_currency}=X"
        exchange_rate = yf.Ticker(currency_pair).history(period="1d")["Close"].iloc[-1]
        return amount * exchange_rate
    except Exception as e:
        return f"❌ Error: {e}"

# Function to fetch historical exchange rates
def get_historical_rates(from_currency, to_currency, start_date, end_date):
    try:
        currency_pair = f"{from_currency}{to_currency}=X"
        data = yf.Ticker(currency_pair).history(start=start_date, end=end_date)
        return data["Close"]
    except Exception as e:
        return f"❌ Error: {e}"

# === Streamlit UI ===
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🔄 Advanced Unit & Currency Converter</h1>",
    unsafe_allow_html=True
)

# Sidebar Styling
st.sidebar.markdown(
    "<h3 style='text-align: center; color: #ff6347;'>⚙️ Select Conversion Type</h3>",
    unsafe_allow_html=True
)

option = st.sidebar.radio("", list(unit_categories.keys()) + ["💰 Currency", "📊 Exchange Rate Trends"])

st.markdown("---")  # Separator

# === Unit Conversion UI ===
if option in unit_categories:
    st.markdown(f"<h3 style='color: #4CAF50;'>{option} Converter</h3>", unsafe_allow_html=True)
    
    value = st.number_input("🔢 Enter Value", min_value=0.0, format="%f")
    
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("🔄 From Unit", unit_categories[option])
    with col2:
        to_unit = st.selectbox("🎯 To Unit", unit_categories[option])
    
    if st.button("🚀 Convert", use_container_width=True):
        result = convert_units(value, from_unit, to_unit)
        if "Error" in str(result):
            st.error(result)
        else:
            st.success(f"✅ Converted Value: **{result} {to_unit}**")

# === Currency Conversion UI ===
elif option == "💰 Currency":
    st.markdown("<h3 style='color: #ff6347;'>💰 Currency Converter</h3>", unsafe_allow_html=True)
    
    amount = st.number_input("💵 Enter Amount", min_value=0.0, format="%f")
    
    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox("🔄 From Currency", currency_codes)
    with col2:
        to_currency = st.selectbox("🎯 To Currency", currency_codes)

    if st.button("💱 Convert", use_container_width=True):
        result = convert_currency(amount, from_currency, to_currency)
        if "Error" in str(result):
            st.error(result)
        else:
            st.success(f"✅ Converted Amount: **{result:.2f} {to_currency}**")

# === Exchange Rate Trends UI ===
elif option == "📊 Exchange Rate Trends":
    st.markdown("<h3 style='color: #ff6347;'>📊 Historical Exchange Rate Trends</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox("🔄 Base Currency", currency_codes, key="hist_from")
    with col2:
        to_currency = st.selectbox("🎯 Target Currency", currency_codes, key="hist_to")
    
    # Preset date range options
    date_range = st.radio("⏳ Select Date Range", ["1 Month", "6 Months", "1 Year", "Custom"], horizontal=True)
    
    if date_range == "1 Month":
        start_date = datetime.today() - timedelta(days=30)
    elif date_range == "6 Months":
        start_date = datetime.today() - timedelta(days=180)
    elif date_range == "1 Year":
        start_date = datetime.today() - timedelta(days=365)
    else:
        start_date = st.date_input("📅 Start Date", datetime.today() - timedelta(days=30))
    
    end_date = datetime.today()
    
    if st.button("📈 Show Trends", use_container_width=True):
        rates = get_historical_rates(from_currency, to_currency, start_date, end_date)
        if isinstance(rates, str) and "Error" in rates:
            st.error(rates)
        else:
            st.line_chart(rates)
            st.success("✅ Exchange rate trends loaded successfully!")

st.markdown(
    "<h4 style='text-align: center; color: #4CAF50;'>🌍 Supports all major units and currencies! 🚀</h4>",
    unsafe_allow_html=True
)
