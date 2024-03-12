from flask import Blueprint, request, render_template
import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import date, datetime, timedelta

import keras
print(keras.__version__)

load_dotenv()

client = StockHistoricalDataClient(os.getenv('API_KEY'), os.getenv('API_SECRET'))

def stock_info_from_range(symbols: list[str], start: datetime, end: datetime):
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )

    apple_bars = client.get_stock_bars(request_params)

    return apple_bars.df

def stock_info_from_day(symbols: list[str], day: datetime):
    end = day + timedelta(days=1)

    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=day,
        end=end
    )

    apple_bars = client.get_stock_bars(request_params)

    return apple_bars.df

serverExample_bp = Blueprint('serverExample', __name__, url_prefix='/serverExample')

@serverExample_bp.route('/helloworld', methods=['GET'])
def helloworld():
    returnDict = { "hello": "world"}
    return returnDict

@serverExample_bp.route('/predictStockData', methods=['POST'])
def useMLModel():
    stock = request.form.get('stock_ticker')
    date_str = request.form.get('date')
    date_input = datetime.strptime(date_str, '%Y-%m-%d')
    if date_input < date_input.today():
        prices = stock_info_from_day([stock], date_input)
        prices.drop(['trade_count', 'vwap'], axis=1, inplace=True)
        return prices.reset_index().to_json()
    else:
        prices = stock_info_from_range([stock], date.today() - timedelta(weeks=15), date.today())
        prices.drop(['trade_count', 'vwap'], axis=1, inplace=True)
        prices_formatted = prices.reset_index().drop(['symbol'], axis=1);
        print(prices_formatted.shape)

        model = keras.models.load_model('./resources/aapl_lstm_model.h5')
        
        return prices.reset_index().to_json()
