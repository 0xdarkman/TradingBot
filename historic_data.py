from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import os.path
import json

APIkey = 'PBO2NQEW58LZWI7U'

ts = TimeSeries(key=APIkey, output_format='pandas')
ti = TechIndicators(key=APIkey, output_format='JSON')
# data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')
# inter_day_data, inter_day_meta_data = ts.get_daily_adjusted(symbol='AAPL', outputsize='full')

SMA_data, SMA_meta_data = ti.get_sma(symbol='AAPL', interval='1min', time_period=60, series_type='open')


print(SMA_data)

dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/historic_data_log/'

path = os.path.join(dirPath, 'historicdata.json')
with open(path, 'w') as json_file:
    json.dump(SMA_data, json_file)