import tensorflow as tf
from tensorflow import keras
import pandas as pd
import datetime
import importlib  

currency = importlib.import_module('api-wrapper.forex')
stock = importlib.import_module('api-wrapper.stock')

def learn(model: tf.keras.Model, ticker: str):
    '''Calls API for recent stock data, saves the current
    state of the model, trains the model on the new data, 
    and then saves the newly created model.'''
    #TODO: Save the current state of the model

    #Call API for stocks
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    new_stock = stock.stock_info_from_range([].append(ticker), start=yesterday, end=today)

    #TODO: Call API for currency
    

    #TODO: Train the model on API data
    model.train_on_batch()

    #TODO: Save new model state
