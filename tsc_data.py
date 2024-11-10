import yfinance as yf
import pandas as pd

# Download historical data for a stock
ticker = 'TCS.NS'
data = yf.download(ticker, start='2020-01-01', end='2023-01-01')

# Save the data to an Excel file
excel_file = 'tcs_stock_data.xlsx'
data.to_excel(excel_file)

print(f"Data has been downloaded and saved to {excel_file}")
