# -*- coding: utf-8 -*-
"""K-foldsModelNoFeatureEngineering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PijH59b0KsR9l4eWxg6KTNYaXgQeNE3C
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install --upgrade keras
import keras
print(keras.__version__)

from google.colab import drive
drive.mount('/content/gdrive', readonly=True)

!pip install -q kaggle
!mkdir -p ~/.kaggle
!cp /content/gdrive/MyDrive/ml-project/kaggle.json ~/.kaggle/
!ls ~/.kaggle
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d andrewmvd/sp-500-stocks

from zipfile import PyZipFile

zipfile = PyZipFile('sp-500-stocks.zip')
zipfile.extractall()

import pandas as pd

import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import KFold

df_stocks = pd.read_csv('sp500_stocks.csv')
sc = MinMaxScaler(feature_range = (0, 1))
scaler = sc.fit(df_stocks[["Close", "High", "Low", "Open", "Volume"]])
df_stocks[["Close", "High", "Low", "Open", "Volume"]] = scaler.transform(df_stocks[["Close", "High", "Low", "Open", "Volume"]])
print(df_stocks[["Close", "High", "Low", "Open", "Volume"]].shape)
df_stocks.drop(labels=['Adj Close'], axis='columns', inplace=True)
df_stocks.dropna(inplace=True)
df_stocks.set_index('Symbol', inplace=True)
grouped = df_stocks.groupby(level=0)
df_stocks_dict = {group: group_df for group, group_df in grouped}

import numpy as np

numdays = 330
windowSize = 60
features = 5

sc = MinMaxScaler(feature_range = (0, 1))
megaDF = []
sizes = []
i = 0
for key in df_stocks_dict:
    temp_df = df_stocks_dict[key][(-1 * windowSize):].copy()  # Create a copy of the DataFrame
    temp_df.drop(columns=temp_df.columns[0], axis=1, inplace=True)

    if(i == 351) :
      print(temp_df)
    i += 1

    if temp_df.shape[0] == windowSize:  # Check if temp_df has the desired number of rows
        megaDF.append(temp_df.values)  # Append the values to megaDF
        sizes.append(windowSize)  # Update the sizes list
    else:
        print(f"Ignoring {key} due to insufficient data for window calculation")
        continue

mega_array = np.array(megaDF)
print(mega_array.shape)
# mode = max(set(sizes), key=sizes.count)
# print(mode)

np.random.seed(42)
tf.random.set_seed(42)

model = keras.models.Sequential([
    keras.layers.LSTM(60, return_sequences=True, input_shape=[None, 5]),
    keras.layers.Dropout(0.15),
    keras.layers.LSTM(60, return_sequences=True),
    keras.layers.Dropout(0.15),
    keras.layers.LSTM(60, return_sequences=False),
    keras.layers.Dropout(0.15),
    keras.layers.Dense(1)
])

model.compile(loss="mse", optimizer="adam")

"""# **Below is cold that utlizes k-folds cross validation**"""

k = 5  # Number of folds
kf = KFold(n_splits=k, shuffle=True, random_state=42)

for train_index, val_index in kf.split(mega_array):
    X_train, X_val = mega_array[train_index], mega_array[val_index]
    y_train, y_val = mega_array[train_index, 4], mega_array[val_index, 4]

    # Perform model training and evaluation using X_train, y_train, X_val, and y_val
for train_index, val_index in kf.split(mega_array):
    X_train, X_val = mega_array[train_index], mega_array[val_index]
    y_train, y_val = mega_array[train_index, 4], mega_array[val_index, 4]

    # Train your model
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val))

    # Evaluate your model
    loss = model.evaluate(X_val, y_val)
    print("Validation Loss:", loss)

model.save("UPDATE_lstm_model.h5")

def plot_series(series, y=None, y_pred=None, x_label="$t$", y_label="$x(t)$", legend=True, title="series"):
    plt.plot(series, ".-")
    if y is not None:
        plt.plot(windowSize, y, "bo", label="Target")
    if y_pred is not None:
        plt.plot(windowSize, y_pred, "rx", markersize=10, label="Prediction")
    plt.grid(True)
    if x_label:
        plt.xlabel(x_label, fontsize=16)
    if y_label:
        plt.ylabel(y_label, fontsize=16, rotation=0)
    plt.title(title)
    if legend and (y or y_pred):
        plt.legend(fontsize=14, loc="upper left")

def plot_learning_curves(loss, val_loss, title):
    plt.plot(np.arange(len(loss)) + 0.5, loss, "b.-", label="Training loss")
    plt.plot(np.arange(len(val_loss)) + 1, val_loss, "r.-", label="Validation loss")
    plt.gca().xaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
    plt.legend(fontsize=14)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title(title)
    plt.grid(True)

print("Evaluation: ")
model.evaluate(X_val, y_val)

plot_learning_curves(history.history["loss"], history.history["val_loss"],
                        "Training and Validation Loss")
plt.show()
plt.savefig('loss.png')

# prompt: using the stocks variable, grab stock data from a specific stock based on a variable. Then store the last x days of stock data where x is equal to the WindowSize variable

# Get the stock data for a specific stock
stock_name = "AAPL"  # Replace with the desired stock name
stock_data = df_stocks_dict[stock_name]

# Store the last WindowSize days of stock data
last_days_data = stock_data[-windowSize:].copy()

# Drop the 'Date' column
last_days_data.drop(columns=['Date'], inplace=True)

last_days_data = np.array(last_days_data)

reshaped_arr = last_days_data.reshape(1, windowSize, 5)
print(reshaped_arr.shape)
testPred = model.predict(reshaped_arr)

print(scaler.inverse_transform(reshaped_arr[0]))
print(testPred)
testPred = [testPred[0][0], 0,0,0,0]
testPred = np.array(testPred)
testPred = testPred.reshape(1, -1)

unscaledPred = scaler.inverse_transform(testPred)
print(unscaledPred[0])

print(X_val.shape)
test = X_val[0]
reshaped_arr = test.reshape(1, windowSize, 5)

print(reshaped_arr[0][0])
print(test[0])

testPred = model.predict(reshaped_arr)
print(testPred)
testPred = [testPred[0][0], 0,0,0,0]
testPred = np.array(testPred)
testPred = testPred.reshape(1, -1)
reshaped_arr = reshaped_arr[0][-1].reshape(1, 5)
print(scaler.inverse_transform(reshaped_arr))
unscaledPred = scaler.inverse_transform(testPred)
print(unscaledPred[0])

plot_series(X_val[0, :, 0], y_val[0, 0], testPred[0, 0], title="prediction")