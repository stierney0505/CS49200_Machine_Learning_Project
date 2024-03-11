# -*- coding: utf-8 -*-
"""midtermModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jsu1vz8h9HXDIKlYtOjT9IfXX6qTRZF_
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

stocks = ["aapl", "amd", "amzn", "msft", "nvda"] #list of stocks in the out.csv file

data_set = pd.read_csv(str(Path.cwd()) + "\\out.csv") #read the csv and grab its data
dataFrames = [] #Array to store the data frames

# For loop to grab each stock's timestamp, open, high, close, volume, trade_count, and the open and close of usd-euro exchange.
# we currently are struggling to develop a model and will add more features as we grow more confident
for stock in stocks :
  df = data_set[["timestamp", "open_"+stock, "high_"+stock, "low_"+stock, "close_"+stock,
         "volume_"+stock, "trade_count_"+stock, "open_eur", "close_eur", ]]
  dataFrames.append(df)

window_size = 10 # Window size for the time series
data = dataFrames[0] # grab just the apple stock data

X = []
y = data[:len(data) - window_size]
# Create the rolling windows for the X set of data
for i in range(len(data) - window_size): 
    X.append(data[i:i+window_size])

X = np.array(X) 

# set up the different data sets to be used in the model
X_train, y_train = X[:int(len(data)*0.7), :window_size], X[:int(len(data)*0.7), 4]
X_valid, y_valid = X[int(len(data)*0.7):int(len(data)*0.9), :window_size], X[int(len(data)*0.7):int(len(data)*0.9), 4]
X_test, y_test = X[int(len(data)*0.9):, :window_size], X[int(len(data)*0.9):, 4]

# print the shapes to ensure they are formatted correctly
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("X_valid shape:", X_valid.shape)
print("y_valid shape:", y_valid.shape)
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)
# method to plot a series and learning curves, taken from the textbook's examples
def plot_series(series, y=None, y_pred=None, x_label="$t$", y_label="$x(t)$", legend=True):
    plt.plot(series, ".-")
    if y is not None:
        plt.plot(window_size, y, "bo", label="Target")
    if y_pred is not None:
        plt.plot(window_size, y_pred, "rx", markersize=10, label="Prediction")
    plt.grid(True)
    if x_label:
        plt.xlabel(x_label, fontsize=16)
    if y_label:
        plt.ylabel(y_label, fontsize=16, rotation=0)
    plt.hlines(0, 0, 100, linewidth=1)
    plt.axis([0, window_size + 1, 0.075, 0.2])
    if legend and (y or y_pred):
        plt.legend(fontsize=14, loc="upper left")
        
def plot_learning_curves(loss, val_loss):
    plt.plot(np.arange(len(loss)) + 0.5, loss, "b.-", label="Training loss")
    plt.plot(np.arange(len(val_loss)) + 1, val_loss, "r.-", label="Validation loss")
    plt.gca().xaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
    plt.legend(fontsize=14)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.grid(True)

np.random.seed(42)
tf.random.set_seed(42)

# Deep Sequential RNN model, the goal is to predict the closing price of the AAPL stock which is the 5th column in the dataframe
model = keras.models.Sequential([
    keras.layers.SimpleRNN(30, return_sequences=True, input_shape=[None, 9]),
    keras.layers.Dropout(0.1), # dropout to reduced overfitting
    keras.layers.SimpleRNN(30, return_sequences=True),
    keras.layers.Dropout(0.1), # dropout to reduced overfitting
    keras.layers.SimpleRNN(30, return_sequences=True),
    keras.layers.Dropout(0.1), # dropout to reduced overfitting
    keras.layers.SimpleRNN(9)
])

model.compile(loss="mse", optimizer="adam")
history = model.fit(X_train, y_train, epochs=50,
                    validation_data=(X_valid, y_valid))

model.evaluate(X_valid, y_valid)

plot_learning_curves(history.history["loss"], history.history["val_loss"])
plt.show()

y_pred = model.predict(X_valid)

plot_series(X_valid[0, :, 4], y_valid[0, 4], y_pred[0, 4])
plt.show()