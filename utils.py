from datetime import datetime
import requests
from config import Settings
import httpx
import json 
import pandas as pd
from dateutil import parser
from collections import OrderedDict

settings = Settings()

def convert_dates(date_string):

    # Define the expected format of the input dates
    EXPECTED_FORMATS = ["%d/%m/%Y", "%d.%m.%Y", '%B %d, %Y']

    # Loop through each expected format and try to convert the date
    for fmt in EXPECTED_FORMATS:
        try:
            date = datetime.strptime(date_string, fmt)
            break
        except ValueError:
            pass
    else:
        # If none of the expected formats work, raise an error
        raise ValueError(f"Date string '{date_string}' does not match any expected format.")
    
    # Convert the date to DD-MM-YYYY format
    formatted_date = date.strftime("%Y-%m-%d")

    return formatted_date

def process_dates(dates):

    if dates is None:
        date_to = datetime.now().date()
        date_from = date_to - pd.Timedelta(days=31)
        
    else:
        # Split the string into two date strings
        date_from, date_to = dates.split("-")
        date_from, date_to = convert_dates(date_from), convert_dates(date_to)

    return date_from, date_to

def get_prices(ticker, dates):
    
    prices_dict = {}

    date_from, date_to = process_dates(dates)

    params = {
      'access_key': settings.API_KEY_MARKETSTACK,
      'date_from': date_from,
      'date_to': date_to
    }

    api_result = httpx.get(f'http://api.marketstack.com/v1/tickers/{ticker}/eod', params=params, verify=False, timeout=50)

    api_response = api_result.json()

    for eod in api_response['data']['eod']:

        date_processed =  parser.parse(eod['date']).strftime('%Y-%m-%d')

        prices_dict[date_processed] = round(eod['close'],1)

    for date in pd.date_range(start=date_from, end=date_to):
        date_str = str(date.date())
        
        # If the date is not in the stock prices dictionary, add it with the previous available stock price as its value
        if date_str not in prices_dict.keys():
            prev_date = str((date - pd.Timedelta(days=1)).date())
            if prev_date not in prices_dict:
                prices_dict[date_str] = 0
            else:
                prices_dict[date_str] = prices_dict[prev_date]

    prices_dict = dict(OrderedDict(sorted(prices_dict.items(), reverse=True)))

    return prices_dict

def get_fx(dates, convert_to):

    date_from, date_to = process_dates(dates)

    fx_rates = list()

    url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={date_from}&end_date={date_to}&base=USD&symbols={convert_to}"

    headers= {
      "apikey": settings.API_KEY_EXCHANGERATESAPI
    }

    response = httpx.get(url, headers=headers, timeout=50)

    result = response.json()

    for date in result['rates']:
        fx_rates.append(result['rates'][date][convert_to])

    return fx_rates


def main(ticker, dates, convert_to):

    prices_dict = get_prices(ticker=ticker, dates=dates)

    fx_rates = get_fx(convert_to=convert_to, dates=dates)

    for i, day in enumerate(prices_dict.keys()):
        # Get the corresponding fx rate from the list
        fx_rate = fx_rates[i]
        
        # Multiply the stock price by the fx rate
        prices_dict[day] *= fx_rate
    
    return prices_dict

