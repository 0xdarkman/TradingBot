import ciso8601 as ciso8601

import matplotlib.pyplot as plt
import json
import pandas as pd
import os
import time

# csvFile = scraper.array2csv_file("NORDNET")
"""df = scraper.read_csv("NORDNET_1589593909.csv", 15)

df.plot(kind='bar', x='NAME', y='CHANGE_%',color='red')
plt.show()"""

dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/HistoricsDataLogs/'
path = os.path.join(dirPath, 'historicdata.json')


with open(path) as json_file:
	data = json.load(json_file)

	df = pd.DataFrame(data)

keys = [key for key in df]
# keysUNIX = [time.mktime(datetime.datetime.strptime(key, "%Y-%m-%d %H:%M").timetuple()) for key in df]
keysUNIX = [time.mktime((ciso8601.parse_datetime(key)).timetuple()) for key in df]
values = [float(value['SMA']) for key, value in data.items()]

keysUNIX.reverse()
values.reverse()
print(keys)
plt.plot(keys, values)
plt.xticks([])
plt.show()
