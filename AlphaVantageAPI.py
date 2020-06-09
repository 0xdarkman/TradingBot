from Scrapers import scraper0
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import os.path

APIkey = 'PBO2NQEW58LZWI7U'

ts = TimeSeries(key=APIkey, output_format='JSON')
ti = TechIndicators(key=APIkey, output_format='JSON')

#data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')
#inter_day_data, inter_day_meta_data = ts.get_daily_adjusted(symbol='AAPL', outputsize='full')
#SMA_data, SMA_meta_data = ti.get_sma(symbol='AAPL', interval='1min', time_period=60, series_type='open')


listings = scraper0.get_combined_listings_data()
tickers = scraper0.check_combined_listings_key_values(listings, "TICKER")
print(tickers)
for ticker in tickers:
	print(str(ticker))
	data, meta_data = ts.get_intraday(symbol=(ticker+".OSL"), interval='15min', outputsize='full')
	print(data)
	print("\n\n")

dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/HistoricsDataLogs/'
path = os.path.join(dirPath, 'historicdata.csv')