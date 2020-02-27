from stockretriever import StockRetriever
from time import sleep
import pymongo

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = db_client["stock_db"]
stocks_collection = db['stocks']
stock_historical_collection = db['stocks_historical']

api_key = 'KEY_GOES_HERE'

#Google, Snap, Uber, Twitter, Pinterest, Microsoft, Capital One, Wallmart, Toyota, General Motors
tickers = ['GOOGL.MI', 'SNAP', 'UBER', 'TWTR', 'PINS', 'MSFT.MI', 'COF', 'WMT', 'TM', 'GM']

retriever = StockRetriever(api_key)

for ticker in tickers:
    retriever.add_ticker(ticker)

#Get and save historical data
if stock_historical_collection.count() == 0:
    data_historical = retriever.get_historical_data()
    for ticker in tickers:
        h_data = data_historical[ticker]['history']
        for s in h_data:
            h_data[s]['date'] = s
            h_data[s]['symbol'] = ticker
            stock_historical_collection.insert_one(h_data[s])


try:
    while True:

        '''
        Data is a dictionary of dictionaries, where the first key is the symbol
        e.g.
        data['GOOGL.MI']['price']
        data['GOOGL.MI']['currency']
        data['GOOGL.MI']['volume']
        data['GOOGL.MI']['price_avg']
        data['GOOGL.MI']['shares']
        data['GOOGL.MI']['day_high']
        data['GOOGL.MI']['price']
        '''

        data = retriever.get_real_time_data()


        #insert in the database
        for ticker in tickers:
            stocks_collection.insert_one(data[ticker])


        #sleep for 10 minutes
        sleep(10 * 60)

except KeyboardInterrupt:
    print('Exiting...')


