import tensorflow as tf
from tensorflow import keras
import pandas as pd
import datetime
import importlib  

currency = importlib.import_module('api-wrapper.forex')
stock = importlib.import_module('api-wrapper.stock')

def do_online_learn(model: tf.keras.Model, ticker: str):
    '''Calls API for recent stock data, saves the current
    state of the model, trains the model on the new data, 
    and then saves the newly created model.'''
    #Call API for stocks
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    new_stock = stock.stock_info_from_range([].append(ticker), start=yesterday, end=today)

    #TODO: Call API for currency
    

    #TODO: Train the model on API data
    model.train_on_batch()

    #Save new model state
    updated_model_name = "Model_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".h5"
    model.save(updated_model_name)
