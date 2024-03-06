import os
from dotenv import load_dotenv
import requests

load_dotenv()
access_key = os.getenv('ACCESS_KEY')

# API from Alpha Vantage
# Limited to 25 requests/day at the free tier

# USD to EUR
url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=EUR&outputsize=full&apikey={access_key}&datatype=csv'

response = requests.get(url)

open('eur.csv', 'wb').write(response.content)

# USD to JPY
url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=JPY&outputsize=full&apikey={access_key}&datatype=csv'

response = requests.get(url)

open('jpy.csv', 'wb').write(response.content)

# USD to AUD
url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=AUD&outputsize=full&apikey={access_key}&datatype=csv'

response = requests.get(url)

open('aud.csv', 'wb').write(response.content)

# USD to CAD
url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=CAD&outputsize=full&apikey={access_key}&datatype=csv'

response = requests.get(url)

open('cad.csv', 'wb').write(response.content)

# USD to CNY
url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=CNY&outputsize=full&apikey={access_key}&datatype=csv'

response = requests.get(url)

open('cny.csv', 'wb').write(response.content)