from Scrapers import scraper0
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from datetime import datetime, timedelta
from collections import OrderedDict
import matplotlib.pyplot as plt

APIkey = 'PBO2NQEW58LZWI7U'

ts = TimeSeries(key=APIkey, output_format='JSON')
ti = TechIndicators(key=APIkey, output_format='JSON')

# data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')
# inter_day_data, inter_day_meta_data = ts.get_daily_adjusted(symbol='AAPL', outputsize='full')
# SMA_data, SMA_meta_data = ti.get_sma(symbol='AAPL', interval='1min', time_period=60, series_type='open')

listings = scraper0.get_combined_listings_data()
tickers = scraper0.check_combined_listings_key_values(listings, "TICKER")
print(tickers)

today_data = {}
for ticker in tickers:
	print(ticker)

	new_data = OrderedDict([])
	# data, meta_data = ts.get_intraday(symbol=(ticker + ".OSL"), interval='1min', outputsize='full')
	data, meta_data = ts.get_daily(symbol=(ticker + ".OSL"), outputsize='full')

	time_format = '%Y-%m-%d %H:%M:%S'
	for key in data:
		date = datetime.strptime(key, time_format) + timedelta(hours=6)
		new_data[str(date)] = data[key]
	today_data[ticker] = new_data

	# print(new_data)
	# print("\n\n")

# print(today_data[tickers[-1]])

print(tickers[0])
x = [key for key in today_data[tickers[0]]]
y = [value["1. open"] for value in today_data[tickers[0]].values()]
print(x)
print("\n")
print(y)

plt.plot(x, y)
xticks = plt.gca().xaxis.get_major_ticks()
for i in range(len(xticks)):
	if i % 100 != 0:
		xticks[i].set_visible(False)

plt.show()
