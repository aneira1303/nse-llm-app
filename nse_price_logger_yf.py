import yfinance as yf
import pandas as pd
from datetime import datetime

# ✅ NSE Tickers
tickers = [
    'RELIANCE.NS',
    'TCS.NS',
    'INFY.NS',
    'ITC.NS',
    'HDFCBANK.NS',
    'KOTAKBANK.NS',
    'ICICIBANK.NS',
    'SBIN.NS',
    'ADANIENT.NS',
    'HINDUNILVR.NS',
    'MARUTI.NS',
    'HDFCAMC.NS',
    'HDFCSML250.NS'  # May or may not return if data is not available intraday
]

# ✅ Fetch intraday data for all tickers
data = yf.download(tickers=tickers, period="1d", interval="1m", group_by='ticker', progress=False)

# ✅ Format and display latest prices
now = datetime.now().strftime("%H:%M:%S")
rows = []

for ticker in tickers:
    try:
        latest_row = data[ticker].dropna().iloc[-1]
        rows.append({
            "Stock": ticker.replace(".NS", ""),
            "Price (₹)": round(latest_row["Close"], 2),
            "Day High": round(data[ticker]["High"].max(), 2),
            "Day Low": round(data[ticker]["Low"].min(), 2),
            "Time": now
        })
    except Exception as e:
        rows.append({
            "Stock": ticker.replace(".NS", ""),
            "Price (₹)": "Error",
            "Day High": "Error",
            "Day Low": "Error",
            "Time": now
        })

# ✅ Display table
df = pd.DataFrame(rows)
print(df)
