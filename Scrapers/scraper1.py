# Scraper for getting current day stock intraday data (can be used for past dates as well) from OSE

import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import json
import pandas as pd
from time import sleep
import math
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys as keys


def get_intraday_today_data(TICKER, DATE="this"): # Date format must be str "YYYY-MM-DD"; no weekends, closed days
	if DATE == "this":
		time_info = datetime.now()
		if time_info.hour < 9:
			raise KeyError("No stock data available for today yet!")
		current_date = time_info.strftime("%Y-%m-%d")
	else:
		current_date = DATE
	URL = "https://www.oslobors.no/ob/servlets/components/graphdata/(PRICE_CA)/TICK/" + TICKER + ".OSE?points=500&stop=" + current_date + "&period=1opendays"

	page_data = requests.get(URL).text
	intraday_data = json.loads(page_data)
	return intraday_data


# X_AXIS => "UNIX" for unix epochs, "TIMESTAMP" for str "YYYY-MM-DD hh:mm:ss", "TIMESTAMP_ROUNDED" for rounded to mins
def process_intraday_data(JSON_INTRADAY, X_AXIS="UNIX", ):
	if "notOkMessage" in JSON_INTRADAY:
		raise KeyError("Did not receive proper data!", JSON_INTRADAY)
	else:
		ticker = JSON_INTRADAY['rows'][0]['key']

	timestamps_prices = JSON_INTRADAY['rows'][0]['values']['series']['c1']['data']
	prices = [y[1] for y in timestamps_prices]
	dataSize = JSON_INTRADAY['rows'][0]['values']['series']['c1']['dataSize']

	if X_AXIS == "UNIX":
		x_axis = [(x[0] // 1000.0) for x in timestamps_prices]
	elif X_AXIS == "TIMESTAMP":
		x_axis = [datetime.fromtimestamp(x[0] // 1000).strftime('%Y-%m-%d %H:%M:%S') for x in timestamps_prices]
	elif X_AXIS == "TIMESTAMP_ROUNDED":
		x_axis = [datetime.fromtimestamp(round(x[0] // 1000 / 60, 0) * 60).strftime('%Y-%m-%d %H:%M:%S') for x in timestamps_prices]
	else:
		x_axis = [(x[0] // 1000.0) for x in timestamps_prices]

	return {'x_axis': x_axis, 'prices': prices, 'dataSize': dataSize}


data = get_intraday_today_data("DNB", DATE="2020-06-08")
data = process_intraday_data(data, X_AXIS="TIMESTAMP_ROUNDED")

print(data)