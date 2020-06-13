# Scraper for checking the most changed stocks at this time
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import time
from time import sleep
import os.path
from selenium import webdriver
import json
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options

"""from selenium.webdriver.common.keys import Keys as keys"""


def get_sec(time_str):
	"""Get Seconds from time."""
	h, m, s = time_str.split(':')
	return int(h) * 3600 + int(m) * 60 + int(s)


def get_listings_data_NORDNET(NUM_OF_LISTINGS=100, SORTED_BY='CHANGE_%'):
	listings_data = []
	listings_data_loop = []
	for idx in range(1, 4):
		URL = "https://www.nordnet.no/market/stocks?selectedTab=prices&sortField=diff_pct&sortOrder=desc&page=" + str(idx) + "&exchangeCountry=NO&exchangeList=no%3Aose"
		stockListingsPage = requests.get(URL).text

		soup = BeautifulSoup(stockListingsPage, 'lxml')
		stockTable = soup.find('tbody', class_='c02372')
		stockListings = stockTable.find_all('tr', class_="c02356 c02375")

		counter = 1
		for listing in stockListings:
			listingInfo = {}

			stockName = (listing.find('td', {'data-title': 'Navn'})).find('a', href=True)
			listingInfo['NAME'] = stockName.decode_contents()
			listingInfo['HREF'] = "https://www.nordnet.no/" + stockName['href']

			try:
				changePercent = (listing.find_all('span', {'class': 'c02421'}))[0].decode_contents().replace("<!-- -->", '').split(" ")
				listingInfo['CHANGE_%'] = float(changePercent[0] + changePercent[1])
			except IndexError:
				listingInfo['CHANGE_%'] = -99

			try:
				changeNOK = (listing.find_all('span', {'class': 'c02421'}))[1].decode_contents().replace("<!-- -->", '').split(
					" ")
				listingInfo['CHANGE_NOK'] = float(changeNOK[0] + changeNOK[1])
			except IndexError:
				listingInfo['CHANGE_NOK'] = -99

			try:
				priceClose = (listing.find_all('span', {'class': 'c02421'}))[2].decode_contents().replace("<!-- -->", '').split(
					" ")
				listingInfo['LAST'] = float(priceClose[1])
			except IndexError:
				listingInfo['LAST'] = -99

			try:
				priceBuy = (listing.find_all('span', {'class': 'c02421'}))[3].decode_contents().replace("<!-- -->", '').split(
					" ")
				listingInfo['BUY'] = float(priceBuy[1])
			except IndexError:
				listingInfo['BUY'] = -99
			try:
				priceSell = (listing.find_all('span', {'class': 'c02421'}))[4].decode_contents().replace("<!-- -->", '').split(
					" ")
				listingInfo['SELL'] = float(priceSell[1])
			except IndexError:
				listingInfo['SELL'] = -99


			priceHigh = (listing.find('td', {'data-title': 'Høy'})).decode_contents().replace(',', '.').replace(' ', '.')
			try:
				listingInfo['HIGH'] = float(priceHigh)
			except Exception:
				"""listingInfo['HIGH'] = priceHigh"""
				continue

			priceLow = (listing.find('td', {'data-title': 'Lav'})).decode_contents().replace(',', '.').replace(' ', '.')
			try:
				listingInfo['LOW'] = float(priceLow)
			except Exception:
				"""listingInfo['LOW'] = priceLow"""
				continue

			revenueMNOK = (listing.find_all('span', {'class': 'c02421'}))[5].decode_contents().replace("<!-- -->",
			                                                                                           '').split(" ")
			listingInfo['REVENUE_MNOK'] = (revenueMNOK[1])

			timeHHMMSS = (listing.find('td', {'data-title': 'Tid'})).find('span').decode_contents()
			listingInfo['TIME_HHMMSS'] = timeHHMMSS
			listingInfo['TIME_SECS'] = get_sec(timeHHMMSS)

			listings_data_loop.append(listingInfo)
		listings_data += listings_data_loop

	listings_data = sorted(listings_data, key=lambda i: i[SORTED_BY])[-NUM_OF_LISTINGS:]
	return listings_data


def get_listings_data_OSLOBORS(NUM_OF_LISTINGS=100, SORTED_BY="VOLUME"):
	URL = "https://www.oslobors.no/ob/servlets/components?type=table&generators%5B0%5D%5Bsource%5D=feed.ose.quotes.EQUITIES%2BPCC&filter=&view=REALTIME&columns=PERIOD%2C+INSTRUMENT_TYPE%2C+TRADE_TIME%2C+ITEM%2C+LONG_NAME%2C+BID%2C+ASK%2C+LASTNZ_DIV%2C+CLOSE_LAST_TRADED%2C+CHANGE_PCT_SLACK%2C+TURNOVER_TOTAL%2C+TRADES_COUNT_TOTAL%2C+MARKET_CAP%2C+PERIOD%2C+TIME%2C+VOLUME_TOTAL&channel=3900cb856640fe3e69a6c0a49d07765c"
	stock_listings_page = requests.get(URL).text
	listings_json = json.loads(stock_listings_page)['rows']

	listings_data = []

	counter = 1
	for listing in listings_json:
		listing_values = listing['values']
		if listing_values['INSTRUMENT_TYPE'] != 'SHARES':
			continue
		listing_info = {}

		listing_info['TICKER'] = listing_values['ITEM']
		listing_info['NAME'] = listing_values['LONG_NAME']

		listing_info['HREF'] = "https://www.oslobors.no/markedsaktivitet/#/details/" + listing_info['TICKER'] + ".OSE/overview"

		listing_info['LAST'] = float(listing_values['LASTNZ_DIV'])
		listing_info['CLOSE_LAST_TRADED_TIME'] = listing_values['CLOSE_LAST_TRADED']

		try:
			listing_info['CHANGE_%'] = float(listing_values['CHANGE_PCT_SLACK'])
		except TypeError:
			listing_info['CHANGE_%'] = -99
		try:
			listing_info['SELL'] = float(listing_values['BID'])
			listing_info['BUY'] = float(listing_values['ASK'])
		except TypeError:
			listing_info['SELL'] = -99
			listing_info['BUY'] = -99

		try:
			listing_info['VOLUME'] = listing_values['VOLUME_TOTAL']
			listing_info['TRADES_COUNT'] = int(listing_values['TRADES_COUNT_TOTAL'])
			listing_info['TURNOVER_MNOK'] = float(listing_values['TURNOVER_TOTAL'] / 1000000.0)
		except TypeError:
			listing_info['VOLUME'] = -99
			listing_info['TRADES_COUNT'] = -99
			listing_info['TURNOVER_MNOK'] = -99

		listing_info['MARKETCAP_MNOK'] = float(listing_values['MARKET_CAP'] / 1000000.0)

		listing_info['TIME_UNIX'] = int(listing_values['TIME'] // 1000)
		listing_info['DATETIME'] = datetime.utcfromtimestamp(listing_values['TIME'] // 1000) + timedelta(hours=2)

		listings_data.append(listing_info)

	listings_data = sorted(listings_data, key = lambda i: i[SORTED_BY])[-NUM_OF_LISTINGS:]
	return listings_data


# USE int: -99 for unknown/invalid data; ORDER_BY => "TRADES_COUNT", "CHANGE_%"
def get_listings_data_OSLOBORS_SELENIUM(NUM_OF_LISTINGS=100, SORTED_BY="VOLUME"):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--window-size=%s" % "1920,1080")

	URL = "https://www.oslobors.no/markedsaktivitet/#/list/shares/quotelist/ose/all/all/false"
	driver = webdriver.Chrome(executable_path='C:/Windows/chromedriver.exe',
	                          chrome_options=chrome_options
	                          )

	while True:
		try:
			driver.get(URL)
			sleep(0.5)
			if SORTED_BY == "TRADES_COUNT":
				driver.find_element_by_xpath(
					'/html/body/div[2]/ui-view/div/ui-view/div[4]/div/ui-view/div/quotes/table/thead/tr/th[13]/span[1]').click()
			elif SORTED_BY == "CHANGE_%":
				driver.find_element_by_xpath(
					'/html/body/div[2]/ui-view/div/ui-view/div[4]/div/ui-view/div/quotes/table/thead/tr/th[8]/span').click()
			break
		except Exception:
			driver.close()

	stockListingsPage = driver.page_source
	soup = BeautifulSoup(stockListingsPage, 'lxml')
	stockTable = soup.find('table', {'class': 'table table-striped stock-list-development'}).find('tbody')
	driver.close()

	stockListings = stockTable.find_all('tr', {'data-reactid': True})

	counter = 1
	listingsData = []
	for listing in stockListings:
		listingInfo = {}
		reactid = listing['data-reactid']

		listingInfo['SECTOR'] = listing.find('td', {'data-reactid': reactid + '.1'})['title']

		listingInfo['TICKER'] = listing.find('a', {'data-reactid': reactid + '.4.0'}).decode_contents()
		listingInfo['NAME'] = listing.find('a', {'data-reactid': reactid + '.5.0'}).decode_contents()
		listingInfo['HREF'] = 'https://www.oslobors.no/markedsaktivitet' + \
		                      listing.find('a', {'data-reactid': reactid + '.5.0'})['href']

		listingInfo['LAST'] = float(
			listing.find('td', {'data-header': 'Siste'}).decode_contents().replace(',', '.').replace(' ', ''))

		changePercent = listing.find('td', {'data-header': 'Avk. % i dag'}).decode_contents().replace(',', '.').replace(
			' ', '')
		try:
			listingInfo['CHANGE_%'] = float(changePercent[:-1])
		except ValueError:
			listingInfo['CHANGE_%'] = -99

		priceSell = listing.find('td', {'data-header': 'Kjøper'}).decode_contents().replace(',', '.').replace(' ', '')
		priceBuy = listing.find('td', {'data-header': 'Selger'}).decode_contents().replace(',', '.').replace(' ', '')
		try:
			listingInfo['SELL'] = float()
			listingInfo['BUY'] = float()
		except ValueError:
			listingInfo['SELL'] = -99
			listingInfo['BUY'] = -99

		listingInfo['TURNOVER_MNOK'] = float(
			listing.find('td', {'data-header': 'Omsatt (MNOK)'}).decode_contents().replace(',', '.').replace(' ', ''))
		listingInfo['TRADES_COUNT'] = int(listing.find('td', {'data-header': 'Ant. handler'}).decode_contents())
		listingInfo['MARKETCAP_MNOK'] = float(
			listing.find('td', {'data-header': 'Markedsverdi (MNOK)'}).decode_contents().replace(',', '.').replace(' ',
			                                                                                                       ''))
		t = time.localtime()
		timeHHMMSS = time.strftime("%H:%M:%S", t)
		listingInfo['TIME_HHMMSS'] = timeHHMMSS
		listingInfo['TIME_SECS'] = get_sec(timeHHMMSS)
		listingInfo['DATETIME'] = listing.find('td', {'data-header': 'Tid'}).decode_contents().replace(',', '.').replace(' ', '')

		listingsData.append(listingInfo)

	listingsData = sorted(get_listings_data_OSLOBORS_SELENIUM(), key=lambda i: i[SORTED_BY])[-NUM_OF_LISTINGS:]
	return listingsData


def get_combined_listings_data(NUM_OF_LISTINGS=1000, SORTED_BY="VOLUME", TOPRINT=False):
	def search_by_value_array_of_dictionaries(KEY, VALUE, ARRAY):
		for dictionary in ARRAY:
			if dictionary[KEY] == VALUE:
				return dictionary

	NORDNET = get_listings_data_NORDNET(NUM_OF_LISTINGS=1000)
	OSE = get_listings_data_OSLOBORS(NUM_OF_LISTINGS=NUM_OF_LISTINGS, SORTED_BY=SORTED_BY)

	combined_listings_data = OSE.copy()
	for idx in range(len(combined_listings_data)):
		listing_name = combined_listings_data[idx]['NAME']
		NORDNET_listing = search_by_value_array_of_dictionaries(KEY='NAME', VALUE=listing_name, ARRAY=NORDNET)
		if NORDNET_listing == None:
			continue
		#print(NORDNET_listing)
		combined_listings_data[idx]["HREF_NORDNET"] = NORDNET_listing["HREF"]
		combined_listings_data[idx]["HIGH"] = NORDNET_listing["HIGH"]
		combined_listings_data[idx]["LOW"] = NORDNET_listing["LOW"]

	if TOPRINT:
		print(combined_listings_data)
	return combined_listings_data


def check_combined_listings_key_values(listings_array, key_to_return):
	info = []
	for listing in listings_array:
		info.append(listing[key_to_return])
	return info


# Scrapes and saves ALL scraped data to file in csv format
# JSON instead?
def get_save_combined_listings_data(NUM_OF_LISTINGS=5):
	dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/_LogsCurrent/'
	listingsData = get_combined_listings_data(NUM_OF_LISTINGS)
	csvName = "SCRAPED_" + str(int(time.time())) + ".csv"
	path = os.path.join(dirPath, csvName)
	with open(path, 'w', newline='', encoding="utf-8") as f:
		w = csv.DictWriter(f, listingsData[0].keys())
		w.writeheader()
		for listing in listingsData:
			w.writerow(listing)
	return csvName


def read_csv(
		*file_rows_columns):  # Returns and prints read csv file. Specify file, columns with (FILENAME, NUMBEROFROWS, "ARG1", "ARG2", ...).
	dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/_LogsCurrent/'
	columnNames = []
	if len(file_rows_columns) == 1:
		columnNames = []
		rows = None
	elif len(file_rows_columns) == 2:
		columnNames = []
		rows = file_rows_columns[1]
	elif len(file_rows_columns) == 0:
		raise ValueError("No arguments specified. Must specify a file name.")
	else:
		rows = file_rows_columns[1]
		counter = 0
		for column in file_rows_columns:
			if counter < 2:
				counter += 1
				continue
			columnNames.append(column)
			counter += 1

	path = os.path.join(dirPath, file_rows_columns[0])
	df = pd.read_csv(path, nrows=rows)
	with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 0):
		if not columnNames:
			columnNames = df.columns
		print(df[columnNames])
		return df


"""listings = get_combined_listings_data(toPrint=True)"""

"""csvFile = get_save_combined_listings_data()
read_csv(csvFile)"""

"""print(next((item for item in NORDNET if item["NAME"] == OBE[-1]["NAME"]), None))"""
