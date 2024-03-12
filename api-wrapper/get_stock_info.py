import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import date, datetime, timedelta

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

def latest_stock_csvs(symbols: list[str]):
  # for up-to-date date
  endDate = date.today()

  # Get Stock information using 1 request
  df = stock_info_from_range(symbols=symbols, start=datetime(2019, 1, 1), end=endDate)

  # Make a dictionary of dataframes where each key is a stock ticker (defined in stocks variable)
  # and each value is the dataframe with that stock's information
  # Note: symbol (stock ticker) is a Multi-Index, not a column value
  df_grouped = df.groupby(level=0)
  dfs_dict = { group: group_df for group, group_df in df_grouped }

  # download each stock dataframe as a CSV file
  for stock in symbols:
    dfs_dict[stock].to_csv(stock.lower() +'.csv')

stocks = ['AAPL', 'AMD', 'AMZN', 'MSFT', 'NVDA']
latest_stock_csvs(stocks)