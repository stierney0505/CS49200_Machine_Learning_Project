import csv
import os
import pandas as pd
import numpy as np
import keras

# Convert stock/currency data into dataframes
# Convert to shape of (Stock, Date, Features)
# Return


def read_dataframes_from_csv(files):
    """Convert a list of CSV files into a list of dataframes that
    only contain the columns ['timestamp', 'open', 'high', 'low', 'close']"""
    dataframes = []
    for file in files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            # Drop any columns that do not match the specified column names
            required_columns = ["timestamp", "open", "high", "low", "close"]
            df = df[required_columns]
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d")
            # Extract the stock/currency name from the file name without extension
            stock_name = os.path.splitext(os.path.basename(file))[0]
            # Add a new column for Stock/Currency
            df["Stock/Currency"] = stock_name
            # Reorder + filter columns
            df = df[["open", "high", "low", "close"]]
            dataframes.append(df)
        else:
            print(f"Warning: {file} does not exist. Skipping.")
    return dataframes


def df_list_to_time_series(dfs):
    """Convert a list of dataframes into an array
    where each element is a timeseries based on the
    timestamp column (0)"""
    timeseries_list = []
    for df in dfs:
        data = np.asarray(df)
        time_df = keras.utils.timeseries_dataset_from_array(
            data=data,
            targets=df["close"],
            sequence_length=7,  # Because the data is 1 day per step in the dataset? Maybe?
            batch_size=32,
        )
        timeseries_list.append(time_df)

    return timeseries_list


csv_files = [
    "AAPL.csv",
    "AMD.csv",
    "AMZN.csv",
    "aud.csv",
    "cad.csv",
    "cny.csv",
    "eur.csv",
    "jpy.csv",
    "MSFT.csv",
    "NVDA.csv",
]

df_list = read_dataframes_from_csv(csv_files)

timeseries = df_list_to_time_series(df_list)

# timeseries_array = np.asanyarray(timeseries)

# print(timeseries[0])

for batch in timeseries[0]:
    print(batch[0].shape)
