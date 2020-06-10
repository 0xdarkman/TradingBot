# Scraper for getting current day stock intraday data (can be used for past dates as well) from OSE

import requests
#from bs4 import BeautifulSoup
#from datetime import date
from datetime import datetime, timedelta
import json
from collections import OrderedDict
#import pandas as pd
#from time import sleep
#import math
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys as keys
import matplotlib.pyplot as plt


# DATA => "PRICE_CA" for price, "VOLUME" for volume
def get_intraday_data_OSE(TICKER, DATA="PRICE_CA", DATE="this"): # Date format must be str "YYYY-MM-DD"; no weekends, closed days
	if DATE == "this":
		time_info = datetime.now()
		if time_info.hour < 9:
			raise KeyError("No stock data available for today yet!")
		current_date = time_info.strftime("%Y-%m-%d")
	else:
		current_date = DATE
	URL = "https://www.oslobors.no/ob/servlets/components/graphdata/(" + DATA + ")/TICK/" + TICKER + ".OSE?points=500&stop=" + current_date + "&period=1opendays"

	page_data = requests.get(URL).text
	intraday_data = json.loads(page_data)
	return intraday_data


def get_intraday_week_data_OSE(TICKER, DATA="PRICE_CA"):
	intraday_week = {}

	current_date = datetime.now()
	if current_date.hour < 9:
		current_date = current_date - timedelta(hours=9)
	week_ago = current_date - timedelta(weeks=1)

	nb_days = (current_date - week_ago).days + 1  # + 1 because range is exclusive
	dates = [week_ago + timedelta(days=x) for x in range(nb_days)]
	dates_no_wkend = [datetime.strftime(d, '%Y-%m-%d') for d in dates if not d.isoweekday() in [6, 7]]

	for date in dates_no_wkend:
		intraday_week[date] = get_intraday_data_OSE(TICKER=TICKER, DATA=DATA, DATE=date)
	return intraday_week


# PERIOD => 1, 3, 6
def get_daily_data_OSE(TICKER, PERIOD=1):
	OHCLV = {}

	time_info = datetime.now()
	if time_info.hour < 9:
		raise KeyError("No stock data available for today yet!")
	current_date = time_info.strftime("%Y-%m-%d")

	OHCLV_names = ["OPEN_CA", "HIGH_CA", "LOW_CA", "CLOSE_CA", "VOLUME"]

	for indicator in OHCLV_names:
		URL = "https://www.oslobors.no/ob/servlets/components/graphdata/(" + indicator + ")/DAY/" + TICKER + ".OSE?points=500&stop=" + current_date + "&period=" + str(PERIOD) + "months"
		page_data = requests.get(URL).text
		OHCLV[indicator] = json.loads(page_data)
	return OHCLV


# X_AXIS => "UNIX" for unix epochs, "TIMESTAMP" for str "YYYY-MM-DD hh:mm:ss", "TIMESTAMP_ROUNDED" for rounded to mins
def process_intraday_data(JSON_VAR, X_AXIS="UNIX"):
	if "notOkMessage" in JSON_VAR:
		raise KeyError("Did not receive proper data!", JSON_VAR)
	else:
		key = JSON_VAR['rows'][0]['key']

	timestamps_prices = JSON_VAR['rows'][0]['values']['series']['c1']['data']
	information = [y[1] for y in timestamps_prices]
	dataSize = JSON_VAR['rows'][0]['values']['series']['c1']['dataSize']

	if X_AXIS == "UNIX":
		x_axis = [(x[0] // 1000.0) for x in timestamps_prices]
	elif X_AXIS == "TIMESTAMP":
		x_axis = [datetime.fromtimestamp(x[0] // 1000).strftime('%Y-%m-%d %H:%M:%S') for x in timestamps_prices]
	elif X_AXIS == "TIMESTAMP_ROUNDED":
		x_axis = [datetime.fromtimestamp(round(x[0] // 1000 / 60, 0) * 60).strftime('%Y-%m-%d %H:%M:%S') for x in timestamps_prices]
	else:
		x_axis = [(x[0] // 1000.0) for x in timestamps_prices]

	return {'x_axis': x_axis, 'y_axis': information, 'dataSize': dataSize, 'key': key}


def process_intraday_week_data(JSON_VAR, X_AXIS="UNIX", SEPARATE_DAYS=True):
	intraday_week = OrderedDict([])
	dataSizes = []
	dataSizeTotal = 0
	for day in JSON_VAR:
		intraday_week[day] = process_intraday_data(JSON_VAR=JSON_VAR[day], X_AXIS=X_AXIS)
		dataSizes.append(intraday_week[day]['dataSize'])
		dataSizeTotal += intraday_week[day]['dataSize']
		key = intraday_week[day]['key']
	if SEPARATE_DAYS:
		return intraday_week
	else:
		x_axis = ([intraday_week[day]['x_axis'] for day in intraday_week])
		y_axis = ([intraday_week[day]['y_axis'] for day in intraday_week])
		joined_x_axis = []
		joined_y_axis = []
		for array in x_axis:
			joined_x_axis += array
		for array in y_axis:
			joined_y_axis += array
		return {'x_axis': joined_x_axis, 'y_axis': joined_y_axis, 'dataSize': dataSizeTotal, 'dataSizes': dataSizes, 'key':key}


# X_AXIS => "UNIX" for unix epochs, "TIMESTAMP" for str "YYYY-MM-DD hh:mm:ss", "TIMESTAMP_ROUNDED" for rounded to mins
def process_daily_data(JSON_VAR, X_AXIS_DAY="UNIX"):
	OHCLV = {}
	for indicator in JSON_VAR:
		OHCLV[indicator] = process_intraday_data(JSON_VAR[indicator], X_AXIS=X_AXIS_DAY)
	return OHCLV


def get_processed_intraday_OSE(TICKER, DATA="PRICE_CA", DATE="this", X_AXIS="UNIX"):
	OSE_intraday = get_intraday_data_OSE(TICKER=TICKER, DATA=DATA, DATE=DATE)
	return process_intraday_data(JSON_VAR=OSE_intraday, X_AXIS=X_AXIS)


def get_processed_intraday_week_OSE(TICKER, DATA="PRICE_CA", X_AXIS="UNIX", SEPARATE_DAYS=True):
	OSE_intraday = get_intraday_week_data_OSE(TICKER=TICKER, DATA=DATA)
	return process_intraday_week_data(JSON_VAR=OSE_intraday, X_AXIS=X_AXIS, SEPARATE_DAYS=SEPARATE_DAYS)


def get_processed_daily_OSE(TICKER, PERIOD=1, X_AXIS_DAY="UNIX"):
	OSE_daily = get_daily_data_OSE(TICKER=TICKER, PERIOD=PERIOD)
	return process_daily_data(JSON_VAR=OSE_daily, X_AXIS_DAY=X_AXIS_DAY)


def create_2_graphs_diff_scales():
	data = (get_processed_daily_OSE("SAS+NOK", X_AXIS_DAY="TIMESTAMP"))

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


"""data = get_processed_daily_OSE("SAS+NOK", X_AXIS_DAY="UNIX")
plt.plot(data['HIGH_CA']['x_axis'], data['HIGH_CA']['y_axis'], marker='o', color='r')
plt.plot(data['LOW_CA']['x_axis'], data['LOW_CA']['y_axis'], marker='o', color='b')
plt.show()"""