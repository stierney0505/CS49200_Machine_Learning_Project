# Python 3.11.3
import os
import zipfile
import pandas
import numpy


#Unzip the data/grab the data? 
#Load data into memory
#Grab relevant data and put it into a dataframe
#Calculate new features from data
#Add new features to the dataframe
#Save dataframe as CSV

#Unzipping data
#Exchange rate dataset: https://www.kaggle.com/datasets/dhruvildave/currency-exchange-rates
#Stock Market Dataset: https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/data 

#NOTE: You will need to rename the stock/currency data to these names specifically for this script to function. 
STOCK_ZIP_NAME = "stock.zip"
CURRENCY_ZIP_NAME = "currency.zip"

if not os.path.isfile(os.path.join(os.getcwd() + "\\preprocessing\\intermediate\\stock\\Data\\Stocks\\a.us.txt")):
    print("Stock data not found, begin unzipping.")
    with zipfile.ZipFile(os.path.join(os.getcwd() + "\\preprocessing\\data\\" + STOCK_ZIP_NAME), 'r') as zippedfile:
        zippedfile.extractall(os.path.join(os.getcwd() + "\\preprocessing\\intermediate\\stock"))
    print("Finished unzipping stock data.")

if not os.path.isfile(os.path.join(os.getcwd() + "\\preprocessing\\intermediate\\currency\\forex.csv")):
    print("Currency file not found, begin unzipping.")
    with zipfile.ZipFile(os.path.join(os.getcwd() + "\\preprocessing\\data\\" + CURRENCY_ZIP_NAME), 'r') as zippedfile:
        zippedfile.extractall(os.path.join(os.getcwd() + "\\preprocessing\\intermediate\\currency"))
    print("Finished unzipping currency data.")
