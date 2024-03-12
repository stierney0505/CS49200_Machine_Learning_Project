import datetime
import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from api_wrapper.get_stock_info import stock_info_from_range

def do_online_learn(ticker: str):
    '''Calls API for recent stock data, saves the current
    state of the model, trains the model on the new data, 
    and then saves the newly created model.'''
    #Load existing model
    try:
        model_path = os.path.join('..', '..', 'model_files', ticker + '_lstm_model_recent.h5')
        model = keras.models.load_model(model_path)
    except OSError:
        model_path = os.path.join('..', '..', 'model_files', ticker + '_lstm_model.h5')
        model = keras.models.load_model(model_path)

    #Call API for stocks
    today = datetime.datetime.now()

    new_stock = stock_info_from_range([ticker], today, today - datetime.timedelta(50))

    #TODO: Call API for currency

    #Scale API data
    cols_to_keep = ["open", "high", "low", "close", "volume", "trade_count"]

    df = new_stock.filter(cols_to_keep)
    sc = MinMaxScaler(feature_range = (0, 1))
    df = df.fit_transform(sc)

    array_data = df.values
    reshaped_array = array_data.reshape(1, 50, 6)
    df.iloc[:, :] = reshaped_array

    #Train the model on API data
    y_df = df.shift(-1) # Shift the DataFrame by one time step to create the target data
    y_df.dropna(inplace=True) # Drop the last row, as it will contain NaN values

    model.train_on_batch(df, y_df)

    #Save new model state
    updated_model_name = ticker + '_lstm_model_recent.h5'
    model.save(updated_model_name)
