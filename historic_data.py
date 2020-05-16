from alpha_vantage.timeseries import TimeSeries
APIkey = 'PBO2NQEW58LZWI7U'
ts = TimeSeries(key=APIkey, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')


print(data)
