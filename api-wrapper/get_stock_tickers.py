import pandas as pd

df = pd.read_csv('sp500_companies.csv')
stock_tickers = df.loc[:, ['Symbol']]
stock_tickers_df = pd.DataFrame(stock_tickers)
stock_tickers.to_csv('accepted_stocks.csv', index=False)