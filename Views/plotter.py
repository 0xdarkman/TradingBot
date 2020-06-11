import ciso8601 as ciso8601
from Scrapers.scraper1 import get_processed_intraday_week_OSE, get_processed_intraday_OSE, get_processed_daily_OSE
import matplotlib.pyplot as plt
from datetime import datetime


def create_2_graphs_diff_scales_OHLCV():
	data = (get_processed_daily_OSE("SAS+NOK", X_AXIS_DAY="DATETIME"))

	fig, ax1 = plt.subplots()
	color = 'tab:red'
	ax1.set_xlabel('today')
	ax1.set_ylabel(ylabel='CLOSE_CA', color=color)
	ax1.plot(data['CLOSE_CA']['x_axis'], data['CLOSE_CA']['y_axis'], marker='o', color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

	color = 'tab:blue'
	ax2.set_ylabel('VOLUME', color=color)  # we already handled the x-label with ax1
	ax2.plot(data['VOLUME']['x_axis'], data['VOLUME']['y_axis'], marker='o', color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.show()


def create_2_graphs_diff_scales_intraday():
	prices = (get_processed_intraday_OSE(TICKER="SAS+NOK", DATA="PRICE_CA", X_AXIS="DATETIME", DATE='2020-06-10'))
	volume = (get_processed_intraday_OSE(TICKER="SAS+NOK", DATA="VOLUME", X_AXIS="DATETIME", DATE='2020-06-10'))

	fig, ax1 = plt.subplots()
	color = 'tab:red'
	ax1.set_xlabel('today')
	ax1.set_ylabel(ylabel='PRICE', color=color)
	ax1.plot(prices['x_axis'], prices['y_axis'], marker='o', color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

	color = 'tab:blue'
	ax2.set_ylabel('VOLUME', color=color)  # we already handled the x-label with ax1
	ax2.plot(volume['x_axis'], volume['y_axis'], marker='o', color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.show()

create_2_graphs_diff_scales_intraday()

"""dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/_LogsHistoric/'
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
"""