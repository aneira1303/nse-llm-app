import yfinance as yf
import openpyxl
from datetime import datetime

# ✅ List of tickers (with .NS for NSE stocks and funds)
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
    'HDFCSML250.NS'  # ✅ HDFC Nifty Smallcap 250 Index Fund
]

# ✅ Output Excel file name
file_name = "nse_price_log.xlsx"

# Try to load existing workbook, or create a new one
try:
    wb = openpyxl.load_workbook(file_name)
    ws = wb.active
except FileNotFoundError:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "NSE Price Log"
    ws.append(["Date", "Time"] + [t.replace('.NS', '') for t in tickers])  # Header row

# Get current timestamp
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M:%S")

# Fetch live prices using yfinance
prices = []
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('regularMarketPrice', 'Error')
        prices.append(price)
    except Exception as e:
        prices.append("Error")

# Write new row into Excel sheet
ws.append([date_str, time_str] + prices)
wb.save(file_name)

print(f"✅ Logged {len(tickers)} stock prices to '{file_name}' at {date_str} {time_str}")
