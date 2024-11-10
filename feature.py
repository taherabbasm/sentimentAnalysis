import pandas as pd
import pandas_ta as ta

# Load the cleaned data
data = pd.read_excel('cleaned_nifty50_stock_data.xlsx', index_col=0)

# Calculate Simple Moving Averages (SMA)
data['SMA_50'] = data['Close'].rolling(window=50).mean()
data['SMA_200'] = data['Close'].rolling(window=200).mean()

# Calculate Exponential Moving Averages (EMA)
data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()

# Calculate Relative Strength Index (RSI)
data['RSI'] = ta.rsi(data['Close'], length=14)

# Calculate MACD
data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = ta.macd(data['Close'], fast=12, slow=26, signal=9)

# Display the data with the new features
print("Data with New Features:")
print(data.tail())

# Save the data with new features to a new Excel file
features_excel_file = 'nifty50_features.xlsx'
data.to_excel(features_excel_file)

print(f"\nData with new features has been saved to {features_excel_file}")
