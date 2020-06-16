import ciso8601 as ciso8601
#from Scrapers.scraper1 import get_processed_intraday_week_OSE, get_processed_intraday_OSE, get_processed_daily_OSE
import matplotlib.pyplot as plt
from Scrapers import NordnetOOPScraper
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


def create_2_graphs_diff_scales_nordnet():
	data = NordnetOOPScraper.main()

	instrument_list = []
	for instrument in data:
		instrument_list.append(instrument)

	instrument_0 = instrument_list[0]
	instrument_1 = instrument_list[1]

	fig, ax1 = plt.subplots()
	color = 'tab:red'
	ax1.set_xlabel(instrument_1)
	ax1.set_ylabel(ylabel='PRICE', color=color)
	ax1.plot(data[instrument_1]['TIME'], data[instrument_1]['CLOSE'], marker='o', color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
	color = 'tab:blue'
	ax2.set_ylabel('VOLUME', color=color)  # we already handled the x-label with ax1
	ax2.plot(data[instrument_0]['TIME'], data[instrument_0]['CLOSE'], marker='o', color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.show()


create_2_graphs_diff_scales_nordnet()