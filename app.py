import streamlit as st
import requests
import yfinance as yf
import os
from dotenv import load_dotenv

# ------------------ LOAD ENV ------------------
load_dotenv()
API_KEY = os.getenv("EXCHANGE_API_KEY")

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Currency & Stock Market Intelligence", layout="centered")

# ------------------ COUNTRY DATA ------------------
COUNTRY_DATA = {
    "Japan": {
        "currency": "JPY",
        "indices": {
            "Nikkei 225": "^N225",
            "TOPIX": "^TOPX"
        },
        "hq": "Tokyo Stock Exchange"
    },
    "India": {
        "currency": "INR",
        "indices": {
            "NIFTY 50": "^NSEI",
            "Sensex": "^BSESN",
            "NIFTY Bank": "^NSEBANK"
        },
        "hq": "National Stock Exchange Mumbai"
    },
    "USA": {
        "currency": "USD",
        "indices": {
            "S&P 500": "^GSPC",
            "Dow Jones Industrial Average": "^DJI",
            "NASDAQ Composite": "^IXIC"
        },
        "hq": "New York Stock Exchange"
    },
    "UK": {
        "currency": "GBP",
        "indices": {
            "FTSE 100": "^FTSE",
            "FTSE 250": "^FTMC"
        },
        "hq": "London Stock Exchange"
    },
    "China": {
        "currency": "CNY",
        "indices": {
            "SSE Composite": "000001.SS",
            "CSI 300": "000300.SS"
        },
        "hq": "Shanghai Stock Exchange"
    },
    "South Korea": {
        "currency": "KRW",
        "indices": {
            "KOSPI": "^KS11",
            "KOSDAQ": "^KQ11"
        },
        "hq": "Korea Exchange Seoul"
    }
}

# ------------------ FUNCTIONS ------------------
def get_exchange_rates(base_currency):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if "conversion_rates" not in data:
            raise ValueError("Invalid API response")

        return {
            "USD": data["conversion_rates"].get("USD", "N/A"),
            "INR": data["conversion_rates"].get("INR", "N/A"),
            "GBP": data["conversion_rates"].get("GBP", "N/A"),
            "EUR": data["conversion_rates"].get("EUR", "N/A"),
        }

    except Exception as e:
        # IMPORTANT: still return a dict
        return {
            "USD": "Unavailable",
            "INR": "Unavailable",
            "GBP": "Unavailable",
            "EUR": "Unavailable",
            "error": str(e)
        }


def get_index_value(symbol):
    try:
        df = yf.download(symbol, period="1d", progress=False, threads=False)
        if df.empty:
            return "Data unavailable"
        return round(df["Close"].iloc[-1], 2)
    except:
        return "Data unavailable"

def get_map_embed(location):
    return f"https://www.google.com/maps?q={location}&output=embed"

# ------------------ STREAMLIT UI ------------------
st.title("🌍 Currency & Stock Market Intelligence")

country = st.selectbox(
    "Select Country",
    list(COUNTRY_DATA.keys())
)

if st.button("Get Details"):
    with st.spinner("Fetching live financial data..."):
        data = COUNTRY_DATA[country]

        # Currency
        st.subheader("💱 Official Currency")
        st.write(data["currency"])

        # Exchange Rates
        st.subheader("📊 Real-Time Exchange Rates (1 Unit)")
        rates = get_exchange_rates(data["currency"])
        st.json(rates)

        # Stock Indices
        st.subheader("📈 Major Stock Indices")
        for index, symbol in data["indices"].items():
            value = get_index_value(symbol)
            st.write(f"**{index}** : {value}")

        # Maps
        st.subheader("📍 Stock Exchange HQ")
        st.components.v1.iframe(
            get_map_embed(data["hq"]),
            width=600,
            height=400
        )
