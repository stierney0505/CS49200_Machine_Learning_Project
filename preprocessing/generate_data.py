# Python 3.11.3
import os
import zipfile
import pandas
import numpy


#Unzip the data/grab the data? X
#Grab relevant data and put it into a dataframe
#Calculate new features from data
#Add new features to the dataframe
#Save dataframe as CSV

#Unzipping data
#Exchange rate dataset: https://www.kaggle.com/datasets/dhruvildave/currency-exchange-rates
#Stock Market Dataset: https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/data

#NOTE: You will need to rename the stock/currency data zip files to these names specifically for this script to function.
STOCK_ZIP_NAME = "stock.zip"
CURRENCY_ZIP_NAME = "currency.zip"

STOCK_PREFIX = os.getcwd() + "\\preprocessing\\intermediate\\stock\\Data\\Stocks\\"
CURRENCY_PREFIX = os.getcwd() + "\\preprocessing\\intermediate\\currency\\"

#Check if stock data has already been unzipped
if not os.path.isfile(os.path.join(STOCK_PREFIX + "a.us.txt")):
    print("Stock data not found, begin unzipping.")
    with zipfile.ZipFile(os.path.join(os.getcwd() + "\\preprocessing\\data\\" + STOCK_ZIP_NAME), 'r') as zippedfile:
        zippedfile.extractall(os.path.join(os.getcwd() + "\\preprocessing\\intermediate\\stock"))
    print("Finished unzipping stock data.")

#Check if currency data has already been unzipped
if not os.path.isfile(os.path.join(CURRENCY_PREFIX + "forex.csv")):
    print("Currency file not found, begin unzipping.")
    with zipfile.ZipFile(os.path.join(os.getcwd() + "\\preprocessing\\data\\" + CURRENCY_ZIP_NAME), 'r') as zippedfile:
        zippedfile.extractall(os.path.join(os.getcwd() + "\\preprocessing\\intermediate\\currency"))
    print("Finished unzipping currency data.")



#Grabbing relevant data for dataframe.
STOCKS_TO_GRAB = ["AAPL", "GOOG", "MSFT", "AMZN"] # Limited list for testing
CURRENCIES_TO_GRAB = ["USD/EUR", "USD/JPY", "USD/AUD", "USD/CAD"] # Means rate of USD to X currency

#NOTE: Date ranges in currency dataset:
# USD/CAD - 2003/09/17 - 2021/08/30
# USD/EUR - 2003/12/01 - 2021/08/30
# USD/JPY - 1996/10/30 - 2021/08/30
# USD/AUD - 2006/05/16 - 2021/08/30

#Convert stock names into their file locations
stock_files = []
for stock in STOCKS_TO_GRAB:
    stock_files.append(STOCK_PREFIX + stock + ".us.txt")

#Turn stockfiles into dataframes
stock_frame_list = []
for file in stock_files:
    df = pandas.read_csv(file)
    stock_frame_list.append(df)

#Turn currency csv into dataframe
currency_df = pandas.read_csv(CURRENCY_PREFIX + "forex.csv")

currency_df['date'] = pandas.to_datetime(currency_df['date'])

# currency_df = currency_df.set_index(['date'])

# Define your date range
start_date = '2004-11-08'
end_date = '2005-02-18'

# Create a boolean mask for rows within the date range
mask = (currency_df['date'] >= start_date) & (currency_df['date'] <= end_date)

# Apply the mask to filter rows within the date range
rows_within_range = currency_df[mask]

# Print or further process the filtered rows
print(rows_within_range)
# print(currency_df.loc['2004-11-08' : '2005-02-18'])

#Concatendate all dataframes
