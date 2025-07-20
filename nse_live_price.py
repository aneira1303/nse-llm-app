from nsetools import Nse

# Initialize NSE object
nse = Nse()

# ✅ Set the NSE stock symbol (without .NS)
ticker = "reliance"  # Try 'tcs', 'infy', 'itc', etc.

# Fetch stock details
try:
    stock_data = nse.get_quote(ticker)
    print("✅ Stock Data Fetched Successfully!\n")
    
    # Display selected information
    print(f"Company: {stock_data['companyName']}")
    print(f"Symbol: {stock_data['symbol']}")
    print(f"Last Traded Price: ₹{stock_data['lastPrice']}")
    print(f"Day High: ₹{stock_data['dayHigh']}")
    print(f"Day Low: ₹{stock_data['dayLow']}")
    print(f"Change (%): {stock_data['pChange']}%")
except Exception as e:
    print("❌ Failed to fetch data:", e)
