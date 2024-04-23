from flask import Blueprint, request, render_template
import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
import keras
from keras.losses import MeanSquaredError

from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR

import io
import base64

import matplotlib as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


load_dotenv()

client = StockHistoricalDataClient(os.getenv('API_KEY'), os.getenv('API_SECRET'))

def stock_info_from_range(symbols: list[str], start: datetime, end: datetime):
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )
    bars = client.get_stock_bars(request_params)
    return bars.df

def stock_info_from_day(symbols: list[str], day: datetime):
    end = day + timedelta(days=1)
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=day,
        end=end
    )
    bars = client.get_stock_bars(request_params)
    return bars.df

def calculate_moving_average(data, window_size=20):
    """
    Calculates the moving average for the specified window size.

    Parameters:
        data (pd.DataFrame): DataFrame with stock data.
        window_size (int): The size of the moving window.

    Returns:
        pd.DataFrame: DataFrame with moving average added as a new column.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def get_model_day(numDays: int):
    if numDays == 1:
        return ('Today', str(numDays) + 'day')
    elif numDays == 2:
        return ('1 Day', str(numDays) + 'day')
    elif numDays >= 2 and numDays <= 5:
        return (str(numDays - 1) + ' Days', str(numDays) + 'day')
    elif numDays <= 14:
        return ('2 Weeks', '10day')
    elif numDays <= 21:
        return ('3 Weeks', '15day')
    elif numDays <= 25:
        return ('1 Month', '20day')
    else:
        return ('1 Month', '20day')

serverExample_bp = Blueprint('serverExample', __name__, url_prefix='/serverExample')

@serverExample_bp.route('/helloworld', methods=['GET'])
def helloworld():
    returnDict = { "hello": "world"}
    return returnDict

@serverExample_bp.route('/predictStockData', methods=['POST'])
def useMLModel():

    # Get form data
    stock = request.form.get('stock_ticker')
    model_type = request.form.get('model-type')
    moving_average = request.form.get('moving-average')
    date_str = request.form.get('date')
    date_input = datetime.strptime(date_str, '%Y-%m-%d')
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    day_diff = (date_input - yesterday).days
    res_str, model_day = get_model_day(day_diff)

    # Any date in the future -> predict using ML
    # Check that the stock is on the allowed list
    allowed_stocks = pd.read_csv('./resources/accepted_stocks.csv')['Symbol'].tolist()
    if stock.upper() not in allowed_stocks:
        return 'Invalid stock ticker'

    # Any date in the past -> output the date's stock information using Alpaca API
    if date_input < today:
        if date_input.weekday() < 5:
            prices = stock_info_from_day([stock], date_input)
            prices.drop(['vwap'], axis=1, inplace=True)
            return prices.reset_index().to_json()
        else:
            return 'Invalid date: Must be a weekend'

    # Get the stock information from the past 25 days 
    # open, high, low, close, volume (possibly moving average)
    if moving_average == 'yes':
        prices = stock_info_from_range([stock], yesterday - timedelta(weeks=15), yesterday)
        prices.drop(['vwap'], axis=1, inplace=True)
        prices_formatted = prices.reset_index().drop(['symbol', 'timestamp'], axis=1)
        prices_fixed = pd.DataFrame({
            'Close': prices_formatted['close'].copy(),
            'High': prices_formatted['high'].copy(),
            'Low': prices_formatted['low'].copy(),
            'Open': prices_formatted['open'].copy(),
            'Volume': prices_formatted['volume'].copy()
        })
        prices_fixed = calculate_moving_average(prices_fixed, 15)
        prices_fixed = prices_fixed[-25:]

        with open('./resources/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        prices_scaled = scaler.transform(prices_fixed)
        prices_scaled = prices_scaled.reshape(1, 25, 6)

        if model_type == 'lstm':
            model_string = './resources/LSTM_MODELS/' + model_day + '_' + model_type + '_MA_model.h5'
        else:
            model_string = './resources/GRU_MODELS/' + model_day + '_' + model_type + '_MA_model.h5'
        print(model_string)
        model = keras.models.load_model(model_string)
        prediction = model.predict(prices_scaled)

        prediction = [prediction[0][0], 0,0,0,0,0]
        prediction = np.array(prediction)
        prediction = prediction.reshape(1, -1)
        prediction_unscaled = scaler.inverse_transform(prediction)
        print(prediction_unscaled[0][0])

        return [res_str, stock.upper(), str(prediction_unscaled[0][0])]
    else:
        prices = stock_info_from_range([stock], yesterday - timedelta(weeks=10), yesterday)
        prices.drop(['vwap'], axis=1, inplace=True)
        prices_formatted = prices.reset_index().drop(['symbol', 'timestamp'], axis=1)
        prices_fixed = pd.DataFrame({
            'Close': prices_formatted['close'].copy(),
            'High': prices_formatted['high'].copy(),
            'Low': prices_formatted['low'].copy(),
            'Open': prices_formatted['open'].copy(),
            'Volume': prices_formatted['volume'].copy()
        })
        prices_fixed = prices_fixed[-25:]

        with open('./resources/scaler_no_MA.pkl', 'rb') as f:
            scaler_no_MA = pickle.load(f)
        prices_scaled = scaler_no_MA.transform(prices_fixed)
        prices_scaled = prices_scaled.reshape(1, 25, 5)

        if model_type == 'lstm':
            model_string = './resources/LSTM_MODELS/no_average/' + model_day + '_' + model_type + '_no_MA_model.h5'
        else:
            model_string = './resources/GRU_MODELS/no_average/' + model_day + '_' + model_type + '_no_MA_model.h5'

        print(model_string)
        model = keras.models.load_model(model_string)
        prediction = model.predict(prices_scaled)
        
        prediction = [prediction[0][0], 0,0,0,0]
        prediction = np.array(prediction)
        prediction = prediction.reshape(1, -1)
        prediction_unscaled = scaler_no_MA.inverse_transform(prediction)
        print(prediction_unscaled[0][0])

        return [res_str, stock.upper(), str(prediction_unscaled[0][0])]

@serverExample_bp.route('/make-plot', methods=['POST'])
def getPlot():
    stock = request.form.get('stock_ticker')

    today = datetime.today()
    numdays = 21

    prices = stock_info_from_range([stock], end=today, start=(today - timedelta(days=numdays)))
    dates = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(numdays)]

    tmp_dates = rrule(
        DAILY,
        byweekday=(MO, TU, WE, TH, FR),
        dtstart=parse(dates[-1]),
        until=parse(dates[0])
    )

    final_dates = [date_.strftime('%Y-%m-%d') for date_ in tmp_dates ]

    # Generate plot
    fig = Figure(facecolor='black')
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title(str(stock) + ' Stock Price from the Past 20 Days')
    axis.set_ylabel("Close Price in USD")
    for tick in axis.get_xticklabels():
        tick.set_rotation(25)
    axis.grid()
    axis.plot(final_dates, prices['close'], "ro-")
    axis.set_facecolor('xkcd:black')
    axis.tick_params(axis='y', colors='white')
    axis.tick_params(axis='x', colors='white')
    axis.yaxis.label.set_color('white')
    axis.title.set_color('white')
    # Save the plot as a file
    filename = 'plot.png'
    filepath = os.path.join('resources', 'static', filename)
    fig.savefig(filepath)

    return ('', 200)