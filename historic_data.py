from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import os.path
import json
import csv

APIkey = 'PBO2NQEW58LZWI7U'

ts = TimeSeries(key=APIkey, output_format='JSON')
ti = TechIndicators(key=APIkey, output_format='JSON')
data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')
# inter_day_data, inter_day_meta_data = ts.get_daily_adjusted(symbol='AAPL', outputsize='full')

#SMA_data, SMA_meta_data = ti.get_sma(symbol='AAPL', interval='1min', time_period=60, series_type='open')


print(data)

dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/historic_data_log/'

path = os.path.join(dirPath, 'historicdata.csv')
"""
with open(path, 'w') as json_file:
    json.dump(data, json_file)
"""
with open(path, 'w', newline='', encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, data[0])
    writer.writeheader()
    for listing in data:
        writer.writerow(listing)