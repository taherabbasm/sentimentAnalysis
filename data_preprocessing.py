import pandas as pd

# Load the data from the Excel file
data = pd.read_excel('nifty50_stock_data.xlsx', index_col=0)

# Display the first few rows of the data
print("Initial Data:")
print(data.head())

# Check for missing values
print("\nMissing Values:")
print(data.isnull().sum())

# Fill missing values with the forward fill method
data.fillna(method='ffill', inplace=True)

# Alternatively, you can fill with mean
# data.fillna(data.mean(), inplace=True)

# Verify that there are no missing values
print("\nMissing Values After Filling:")
print(data.isnull().sum())

# Display the cleaned data
print("\nCleaned Data:")
print(data.head())

# Save the cleaned data to a new Excel file
cleaned_excel_file = 'cleaned_nifty50_stock_data.xlsx'
data.to_excel(cleaned_excel_file)

print(f"\nCleaned data has been saved to {cleaned_excel_file}")
