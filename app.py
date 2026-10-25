import streamlit as st
import yfinance as yf
import pandas as pd

# Streamlit Title
st.set_page_config(page_title = "Fintech Backtester", layout = "wide")
st.title("DCA vs. Lump Sum Backtester")

# Frontend UI
col1, col2, col3 = st.columns(3)
with col1:
  tickers = st.multiselect("Select Assets", ["AAPL", "MSFT", "GOOGL", "AMZN", "BTC-USD"], default=["APPL", "BTC-USD"])
with col2:
  budget = st.number_input("Total Investment ($)", min_value=100.0, value=5000.0, step=100.0)
with col3:
  period = st.selectbox("Time Period", ["6mo", "1y", "2y", "5y"])

if st.button("Run Backtest"):
  results = []

# runs through tickers and runs simulation
for ticker in tickers:
  asset = yf.Ticker(ticker)
  history = asset.history(period=period)

  if history.empty:
    st.warning(f"No data found for {ticker}")
    continue

  real_prices = history['Close'].tolist()

  # lump sum math
  lump_sum_shares = budget / real_prices[0]
  lump_sum_value = lump_sum_shares * real_prices[-1]

  # DCA math
  daily_installment = budget / len(real_prices)
  dca_shares = sum([daily_installment / p for p in real_prices])
  dca_value = dca_shares * real_prices[-1]

  # storing results
  results.append({
    "Asset": ticker,
    "Lump Sum Value ($)": round(lump_sum_value, 2),
    "DCA Value ($)": round(dca_value, 2),
    "Difference ($)": round(abs(lump_sum_value - dca_value), 2),
    "Winning Strategy": "Lump Sum" if lump_sum_value > dca_value else "DCA"
  })

# displays results as clean dataframe
if results:
  st.dataframe(pd.DataFrame(results), use_container_width=True)
    

