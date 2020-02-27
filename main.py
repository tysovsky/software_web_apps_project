from stockretriever import StockRetriever
from time import sleep

api_key = 'KEY_GOES_HERE'

#Google, Snap, Uber, Twitter, Pinterest, Microsoft, Capital One, Wallmart, Toyota, General Motors
tickers = ['GOOGL.MI', 'SNAP', 'UBER', 'TWTR', 'PINS', 'MSFT.MI', 'COF', 'WMT', 'TM', 'GM']

retriever = StockRetriever(api_key)

for ticker in tickers:
    retriever.add_ticker(ticker)

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
        data['GOOGL.MI']['day_low']
        '''

        data = retriever.get_real_time_data()

        #insert in the database
        print(data)

        #sleep for 10 minutes
        sleep(10 * 60)

except KeyboardInterrupt:
    print('Exiting...')


