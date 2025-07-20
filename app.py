import gradio as gr
import pandas as pd
import yfinance as yf
from datetime import datetime
import pytz
import os

CSV_FILE = "portfolio.csv"

# Load portfolio if exists
if os.path.exists(CSV_FILE):
    portfolio = pd.read_csv(CSV_FILE)
else:
    portfolio = pd.DataFrame(columns=["Ticker", "Quantity", "Investment ₹"])

# Save portfolio
def save_portfolio(df):
    df.to_csv(CSV_FILE, index=False)

# Main calculation logic
def calculate_portfolio(df):
    if df.empty:
        return pd.DataFrame(columns=[
            "Ticker", "Quantity", "Investment ₹", "Live Price ₹", "Current Value ₹", 
            "Profit/Loss ₹", "Profit %", "Prev Close ₹", "Change ₹", "Time"
        ])

    df = df.dropna(subset=["Ticker"])  # Ensure valid tickers
    tickers = df["Ticker"].tolist()

    try:
        data = yf.download(tickers=tickers, period="2d", interval="1d", group_by="ticker", progress=False, threads=False)
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

    result = []
    for _, row in df.iterrows():
        ticker = row["Ticker"]
        qty = float(row["Quantity"])
        investment = float(row["Investment ₹"])

        try:
            ticker_data = data[ticker] if isinstance(data.columns, pd.MultiIndex) else data
            latest = ticker_data.iloc[-1]
            previous = ticker_data.iloc[-2]

            live_price = float(latest["Close"])
            prev_close = float(previous["Close"])
            change = round(live_price - prev_close, 2)
            current_value = round(live_price * qty, 2)
            profit_loss = round(current_value - investment, 2)
            profit_percent = round((profit_loss / investment) * 100, 2) if investment else 0.0
        except Exception:
            # If error (e.g., delisted stock), return "-" for all calculated fields
            live_price = prev_close = change = current_value = profit_loss = profit_percent = "-"

        result.append({
            "Ticker": ticker,
            "Quantity": qty,
            "Investment ₹": investment,
            "Live Price ₹": live_price,
            "Current Value ₹": current_value,
            "Profit/Loss ₹": profit_loss,
            "Profit %": profit_percent,
            "Prev Close ₹": prev_close,
            "Change ₹": change,
            "Time": now
        })

    save_portfolio(df)
    return pd.DataFrame(result)

# Add a new blank row
def add_row(df):
    new_row = pd.DataFrame([{"Ticker": "", "Quantity": 0, "Investment ₹": 0.0}])
    return pd.concat([df, new_row], ignore_index=True)

# Gradio UI
with gr.Blocks(title="📈 NSE Live Stock Tracker") as app:
    gr.Markdown("## 📈 NSE Live Stock Portfolio Tracker")

    with gr.Row():
        input_table = gr.Dataframe(
            value=portfolio,
            headers=["Ticker", "Quantity", "Investment ₹"],
            datatype=["str", "number", "number"],
            interactive=True,
            label="📥 Input Your Stocks"
        )

    with gr.Row():
        add_button = gr.Button("➕ Add Stock")
        calc_button = gr.Button("📊 Calculate")

    output_table = gr.Dataframe(
        headers=[
            "Ticker", "Quantity", "Investment ₹", "Live Price ₹", "Current Value ₹",
            "Profit/Loss ₹", "Profit %", "Prev Close ₹", "Change ₹", "Time"
        ],
        datatype=["str", "number", "number", "str", "str", "str", "str", "str", "str", "str"],
        interactive=False,
        label="📊 Portfolio Summary"
    )

    add_button.click(add_row, inputs=input_table, outputs=input_table)
    calc_button.click(calculate_portfolio, inputs=input_table, outputs=output_table)

# Launch locally with public link
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=8080)

