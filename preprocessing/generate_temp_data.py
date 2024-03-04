# Python 3.11.3
import os
import zipfile
import pandas
from sklearn.preprocessing import MinMaxScaler

# This script uses the Kaggle datasets to generate a dataset that will be used for testing until
# our continuous data gathering method is done. 

# pylint: disable=locally-disabled, line-too-long

# Unzip the data/grab the data? X
# Grab relevant data and put it into a dataframe
# Calculate new features from data
# Add new features to the dataframe
# Save dataframe as CSV

###
# Unzipping data
###

# Exchange rate dataset: https://www.kaggle.com/datasets/dhruvildave/currency-exchange-rates
# Stock Market Dataset: https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/data

# NOTE: You will need to rename the stock/currency data zip files to these names specifically for this script to function.
STOCK_ZIP_NAME = "stock.zip"
CURRENCY_ZIP_NAME = "currency.zip"

STOCK_PREFIX = os.getcwd() + "\\preprocessing\\intermediate\\stock\\Data\\Stocks\\"
CURRENCY_PREFIX = os.getcwd() + "\\preprocessing\\intermediate\\currency\\"

# Check if stock data has already been unzipped
if not os.path.isfile(os.path.join(STOCK_PREFIX + "a.us.txt")):
    print("Stock data not found, begin unzipping.")
    with zipfile.ZipFile(os.path.join(os.getcwd() + "\\preprocessing\\data\\" + STOCK_ZIP_NAME), 'r') as zippedfile:
        zippedfile.extractall(os.path.join(
            os.getcwd() + "\\preprocessing\\intermediate\\stock"))
    print("Finished unzipping stock data.")

# Check if currency data has already been unzipped
if not os.path.isfile(os.path.join(CURRENCY_PREFIX + "forex.csv")):
    print("Currency file not found, begin unzipping.")
    with zipfile.ZipFile(os.path.join(os.getcwd() + "\\preprocessing\\data\\" + CURRENCY_ZIP_NAME), 'r') as zippedfile:
        zippedfile.extractall(os.path.join(
            os.getcwd() + "\\preprocessing\\intermediate\\currency"))
    print("Finished unzipping currency data.")

###
# Converting currency data to dataframes
###

CURRENCIES_TO_GRAB = [
    "USD/EUR",
    "USD/JPY",
    "USD/AUD",
    "USD/CAD"]  # Means rate of USD to X currency

# NOTE: Date ranges in currency dataset:
# USD/CAD - 2003/09/17 - 2021/08/30
# USD/EUR - 2003/12/01 - 2021/08/30
# USD/JPY - 1996/10/30 - 2021/08/30
# USD/AUD - 2006/05/16 - 2021/08/30

# Turn currency csv into dataframe
currency_df = pandas.read_csv(CURRENCY_PREFIX + "forex.csv")
currency_df['date'] = pandas.to_datetime(currency_df['date'])

# Define date range
START_DATE = '2006-05-16'
END_DATE = '2020-01-01'

# Create a boolean mask for rows within the date range
currency_date_mask = (currency_df['date'] >= START_DATE) & (currency_df['date'] <= END_DATE)
intermediate_currency_df = currency_df[currency_date_mask]

# Boolean mask for separating into different currencies
currency_frame_list = []
for currency in CURRENCIES_TO_GRAB:
    mask = intermediate_currency_df['slug'] == currency
    currency_frame_list.append(intermediate_currency_df[mask])

###
# Converting stock data to dataframe
###

# Convert stock names into their file locations
STOCKS_TO_GRAB = ["AAPL", "GOOGL", "MSFT", "AMZN"]  # Limited list for testing

stock_files = []
for stock in STOCKS_TO_GRAB:
    stock_files.append(STOCK_PREFIX + stock + ".us.txt")


# Turn stockfiles into dataframes
stock_frame_list = []
for file in stock_files:
    df = pandas.read_csv(file)
    df['Date'] = pandas.to_datetime(df['Date'])
    df.rename(columns={'Date' : 'date'}, inplace=True)
    df.drop(columns=['OpenInt'], inplace=True)
    stock_date_mask = (df['date'] >= START_DATE) & (df['date'] <= END_DATE)
    stock_frame_list.append(df[stock_date_mask])

###
# Concatendate all dataframes
###

final_df = pandas.DataFrame()
i = 0
for stock in stock_frame_list:
    try:
        final_df = final_df.merge(right=stock, on='date', suffixes=('', '_' + STOCKS_TO_GRAB[i]))
    except KeyError:
        #catches first pass where final_df is empty
        final_df = stock
    i += 1

i = 0
for currency in currency_frame_list:
    final_df = final_df.merge(right=currency, on='date', suffixes=('', '_' + CURRENCIES_TO_GRAB[i]))
    i += 1

###
# Data normalization/manipulation
###

# Dropping unnecessary columns that are just the currency name/stock name
columns_to_drop = [col for col in final_df.columns if col.startswith('slug') or col.startswith('currency')]
final_df.drop(columns=columns_to_drop, inplace=True)

scaler = MinMaxScaler()

#Convert Date column into numeric
final_df['date'] = pandas.to_numeric(pandas.to_datetime(final_df['date']))

final_df[final_df.columns] = scaler.fit_transform(final_df)


print(final_df.shape)

try:
    final_df.to_csv(os.path.join(os.getcwd() + '\\preprocessing\\output\\output.csv'), index=False)
    print("DataFrame successfully written to CSV")
except Exception as e:
    print("Error writing DataFrame to CSV:", str(e))
