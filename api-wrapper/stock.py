import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

load_dotenv()

# API from Alpaca (website: https://docs.alpaca.markets/docs/getting-started)
# Limited to 200 calls/min at the free tier
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

# Example calls
# df = stock_info_from_range(['AAPL'], start=datetime(2024, 1, 17), end=datetime(2024, 1, 24))
# print(df.head())

# df = stock_info_from_day(['AAPL'], datetime(2024, 2, 1))
# print(df.head())