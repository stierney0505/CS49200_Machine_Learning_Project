import csv
import os
import pandas as pd

# Convert stock/currency data into dataframes
# Convert to shape of (Stock, Date, Features)
# Return 

def read_dataframes_from_csv(files):
    """Convert a list of CSV files into a list of dataframes that
    only contain the columns ['timestamp', 'open', 'high', 'low', 'close']"""
    dataframes = {}
    for file in files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            # Drop any columns that do not match the specified column names
            required_columns = ['timestamp', 'open', 'high', 'low', 'close']
            df = df[required_columns]
            # Extract the stock/currency name from the file name without extension
            stock_name = os.path.splitext(os.path.basename(file))[0]
            # Add a new column for Stock/Currency
            df['Stock/Currency'] = stock_name
            # Reorder columns
            df = df[['Stock/Currency', 'timestamp', 'open', 'high', 'low', 'close']]
            dataframes[stock_name] = df
        else:
            print(f"Warning: {file} does not exist. Skipping.")
    return dataframes

csv_files = ['AAPL.csv', 'AMD.csv', 'AMZN.csv', 'aud.csv', 'cad.csv', 'cny.csv', 'eur.csv', 'jpy.csv', 'MSFT.csv', 'NVDA.csv']

dataframes = read_dataframes_from_csv(csv_files)

combined_df = pd.concat(dataframes.values(), ignore_index=True)

print(combined_df.shape)
