# from google.colab import drive
# drive.mount('/content/gdrive', readonly=True)

# !pip install -q kaggle
# !mkdir -p ~/.kaggle
# !cp /content/gdrive/MyDrive/ml-project/kaggle.json ~/.kaggle/
# !ls ~/.kaggle
# !chmod 600 ~/.kaggle/kaggle.json

# !kaggle datasets download -d andrewmvd/sp-500-stocks

from zipfile import PyZipFile

zipfile = PyZipFile('sp-500-stocks.zip')
zipfile.extractall()

import pandas as pd

df_stocks = pd.read_csv('sp500_stocks.csv')
df_stocks.drop(labels=['Adj Close'], axis='columns', inplace=True)
df_stocks.dropna(inplace=True)
df_stocks.set_index('Symbol', inplace=True)
grouped = df_stocks.groupby(level=0)
df_stocks_dict = {group: group_df for group, group_df in grouped}