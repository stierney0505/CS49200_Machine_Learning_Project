from flask import Blueprint, request, render_template
import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import date, datetime, timedelta
import numpy as np

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
    # Get form data
    stock = request.form.get('stock_ticker')
    date_str = request.form.get('date')
    date_input = datetime.strptime(date_str, '%Y-%m-%d')

    # Any date in the past -> output the date's stock information using Alpaca API
    if date_input.date() < date.today():
        prices = stock_info_from_day([stock], date_input)
        prices.drop(['vwap'], axis=1, inplace=True)
        return prices.reset_index().to_json()
    # Any date in the future -> predict using ML
    # Check that the stock is on the allowed list
    allowed_stocks = ['aapl', 'amd', 'amzn', 'msft', 'nvda']
    if stock.lower() not in allowed_stocks:
        return 'Invalid stock ticker'
    import keras
    from sklearn.preprocessing import MinMaxScaler
    # Get the stock information from the past 50 days 
    # open, high, low, close, volume
    prices = stock_info_from_range([stock], date(year=2024, month=3, day=11) - timedelta(weeks=15), date(year=2024, month=3, day=11))
    prices.drop(['vwap'], axis=1, inplace=True)
    prices_formatted = prices.reset_index().drop(['symbol', 'timestamp'], axis=1)
    prices_formatted = prices_formatted[-50:]
    # Load the model
    model = keras.models.load_model('./resources/' + stock.lower() + '_lstm_model.keras')
    # Scale the stock data
    scaler = MinMaxScaler(feature_range=(0, 1))
    df = scaler.fit_transform(prices_formatted)
    data_arr = np.array(df)
    reshaped_arr = data_arr.reshape(1, 50, 6)
    
    # Predict using the ML model
    prediction = model.predict(reshaped_arr)
    # Unscale the data and return the data as a response
    unscaled = scaler.inverse_transform(prediction)
    outputList = [stock, date_str]
    outputList.extend(unscaled[0].tolist())
    return outputList

@serverExample_bp.route('/make-plot', methods=['POST'])
def getPlot():
    stock = request.form.get('stock_ticker')
    date_str = request.form.get('date')

    today = datetime.today()
    numdays = 7

    prices = stock_info_from_range([stock], end=today, start=(today - timedelta(days=numdays)))
    dates = [(today - timedelta(days=x)) for x in range(numdays)]

    date_strings = []
    for date in dates:
        date_strings.append(datetime.strptime(date, '%Y-%m-%d')) # Just hope it works man

    # Generate plot
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title(str(stock))
    axis.set_xlabel("Date")
    axis.set_ylabel("Close in USD")
    axis.grid()
    axis.plot(date_strings, prices['close'], "ro-")
    
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return render_template("image.html", image=pngImageB64String)

