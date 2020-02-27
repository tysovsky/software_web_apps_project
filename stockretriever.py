import requests
import json
from enum import Enum

class StockSource(Enum):
    WORLD_TRADING_DATA = 0

class StockRetriever:
    def __init__(self, api_key, source: StockSource = StockSource.WORLD_TRADING_DATA):
        self.api_key = api_key
        self.tickers = []
        self.source = source

    def add_ticker(self, ticker):
        self.tickers.append(ticker)

    def remove_ticker(self, ticker):
        if ticker in self.tickers:
            self.tickers.remove(ticker)

    def clear_tickers(self):
        self.tickers.clear()

    def get_real_time_data(self):
        data = {}

        if self.source == StockSource.WORLD_TRADING_DATA:

            ticker_batch = []
            

            for i, ticker in enumerate(self.tickers):
                ticker_batch.append(ticker)

                if (i + 1) % 5 == 0 or i + 1 == len(self.tickers):
                    url = 'https://api.worldtradingdata.com/api/v1/stock'
                    params = {
                    'symbol': ','.join(ticker_batch),
                    'api_token': self.api_key
                    }
                    response = requests.request('GET', url, params=params)
                    j = response.json()

                    for d in j['data']:
                        data[d['symbol']] = d

                    ticker_batch.clear()
            
        return data

    def get_intraday_data(self, interval = 1, range = 1):
        data = {}

        if self.source == StockSource.WORLD_TRADING_DATA:
            url = 'https://intraday.worldtradingdata.com/api/v1/intraday'

            for i, ticker in enumerate(self.tickers):
                params = {
                    'symbol': ticker,
                    'api_token': self.api_key,
                    'interval': str(interval),
                    'range': str(range)
                }
                response = requests.request('GET', url, params=params)
                j = response.json()

                data[ticker] = j

        
        return data

    def get_historical_data(self, date_from = None, date_to = None):
        data = {}

        if self.source == StockSource.WORLD_TRADING_DATA:
            url = 'https://api.worldtradingdata.com/api/v1/history'

            for ticker in self.tickers:
                params = {
                    'symbol': ticker,
                    'api_token': self.api_key
                }

                if date_from != None:
                    params['date_from'] = date_from

                if date_to != None:
                    params['date_to'] = date_to

                response = requests.request('GET', url, params=params)
                j = response.json()

                data[ticker] = j

        return data

    