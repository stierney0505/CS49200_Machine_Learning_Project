import csv
import os
import pandas as pd
import numpy as np
import keras
from sklearn.preprocessing import MinMaxScaler


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


def calculate_rsi(dataframe):
    '''Calculates the relative strength index of
    a stock from its dataframe.'''
    change = dataframe['close'].diff()
    change.dropna(inplace=True)

    change_up = change.copy()
    change_down = change.copy()

    change_up[change_up < 0] = 0
    change_down[change_down > 0] = 0

    avg_up = change_up.rolling(14).mean()
    avg_down = change_down.rolling(14).mean().abs()

    rsi = 100 * avg_up / (avg_up + avg_down)

    return rsi


def preprocess_dataframes(dataframes, scaler):
    '''Takes in a list of dataframes and 
    applies a rolling average and 
    MinMax scaling.'''

    # RSI calculation

    for frame in dataframes:
        frame['rsi'] = calculate_rsi(frame)

    # Rolling/Moving Average
    moving_average_window = 10

    for frame in dataframes:
        for col in frame:
            frame[col] = frame[col].rolling(moving_average_window).mean()

    # Min-Max scaling (Normalization)
    for frame in dataframes:
        frame[frame.columns] = scaler.fit_transform(frame)

    # Drop NA values
    for frame in dataframes:
        frame.dropna(inplace=True)

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
            sequence_length=5,  # Number of days in one batch.
            batch_size=32,  # Number of sequences of length 'sequence_length' in one 'element' of the timeseries
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

sc = MinMaxScaler()
df_list = preprocess_dataframes(df_list, sc)

timeseries = df_list_to_time_series(df_list)

# print(timeseries[0])

for batch in timeseries[0]:
    print(batch[0])
