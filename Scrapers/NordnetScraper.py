import requests
import SECRETS
import json
import sys
from time import sleep
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Scripts.TextColors import TextColors


def print_request_info(REQUEST_VARIABLE, REQUEST_DESCRIPTION, PRINT_CONTENTS=True):
	statusColor = ""
	if 200 <= int(REQUEST_VARIABLE.status_code) < 300:
		statusColor = TextColors.OKGREEN + str(REQUEST_VARIABLE.status_code) + TextColors.ENDC
	elif 300 <= int(REQUEST_VARIABLE.status_code) < 400:
		statusColor = TextColors.WARNING + str(REQUEST_VARIABLE.status_code) + TextColors.ENDC
	elif 400 <= int(REQUEST_VARIABLE.status_code) < 500:
		statusColor = TextColors.FAIL + str(REQUEST_VARIABLE.status_code) + TextColors.ENDC
	elif 500 <= int(REQUEST_VARIABLE.status_code) < 600:
		statusColor = TextColors.OKBLUE + str(REQUEST_VARIABLE.status_code) + TextColors.ENDC

	if PRINT_CONTENTS:
		print(TextColors.HEADER, str(REQUEST_DESCRIPTION), TextColors.ENDC, "\n\n",
		      "Status Code:\n", statusColor, "\n\n",
		      "Req Headers:\n", REQUEST_VARIABLE.request.headers, "\n\n",
		      "Res Headers:\n", REQUEST_VARIABLE.headers, "\n\n",
		      "Res Cookies:\n", REQUEST_VARIABLE.cookies, "\n\n",
		      "Res Content:\n", REQUEST_VARIABLE.content,
		      "\n\n\n")
	else:
		print(TextColors.HEADER, str(REQUEST_DESCRIPTION), TextColors.ENDC, "\n\n",
		      "Status Code:\n", statusColor, "\n\n",
		      "Req Headers:\n", REQUEST_VARIABLE.request.headers, "\n\n",
		      "Res Headers:\n", REQUEST_VARIABLE.headers, "\n\n",
		      "Res Cookies:\n", REQUEST_VARIABLE.cookies,
		      "\n\n\n")

def now_string(HHMMSS=True, MILLIS=True):
	if MILLIS and HHMMSS:
		return datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f:")
	elif HHMMSS and not MILLIS:
		return datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
	else:
		return datetime.now().strftime("%d-%m-%Y")

def calculate_back_days(DATE="this", PERIOD="0d", JUST_DATETIME=True, TO_STRING=True):
	back_date = 0

	if DATE == "this":
		current_date = datetime.now()
	else:
		current_date = datetime.strptime(DATE, "%Y-%m-%d %H:%M:%S")
	if current_date.hour < 9:
		current_date = current_date - timedelta(hours=9)

	time_integer = int(PERIOD[0])
	period = PERIOD[1]

	if period == 'd':
		back_date = current_date - timedelta(days=time_integer)
	elif period == 'w':
		back_date = current_date - timedelta(weeks=time_integer)
	elif period == "m":
		back_date = current_date - relativedelta(months=time_integer)
	elif period == "y":
		if time_integer > 10:
			print("Cannot get historical data older than 10 years. Setting to 10 years.")
			time_integer = 10
		back_date = current_date - relativedelta(months=time_integer * 12)

	if JUST_DATETIME:
		if TO_STRING:
			return datetime.strftime(back_date, '%Y-%m-%d')
		else:
			return back_date

	nb_days = (current_date - back_date).days + 1  # + 1 because range is exclusive
	dates = [back_date + timedelta(days=x) for x in range(nb_days)]
	dates_no_wkend = [datetime.strftime(d, '%Y-%m-%d') for d in dates if not d.isoweekday() in [6, 7]]

	return dates_no_wkend


# Logging/saving
def save_to_json_file(DATA_DICT, FOLDER, NAME):
	with open('C:\\Users\\theba\\PycharmProjects\\StockTradingBot\\' + FOLDER + '\\' + NAME + '_' + now_string(MILLIS=False) + '.json', 'w') as file:
		file.write(json.dumps(DATA_DICT))
def save_instrument_listings(DATA_DICT, NAME='listings'):
	save_to_json_file(DATA_DICT=DATA_DICT, FOLDER='_LogsListings', NAME=NAME)
def update_transaction_file(DATA_DICT, ORDER):
	json_var = {}

	try:
		with open('C:\\Users\\theba\\PycharmProjects\\StockTradingBot\\_LogsTransactions\\transactions_' + now_string(HHMMSS=False) + '.json', 'r') as file:
			json_var = json.loads(file.read())

	except FileNotFoundError:
		json_var['BOUGHT'] = []
		json_var['SOLD'] = []

	if ORDER == 'BUY':
		json_var['BOUGHT'].append(DATA_DICT)
	elif ORDER == 'SELL':
		json_var['SOLD'].append(DATA_DICT)

	with open('C:\\Users\\theba\\PycharmProjects\\StockTradingBot\\_LogsTransactions\\transactions_' + now_string(HHMMSS=False) + '.json', 'w') as file:
		file.write(json.dumps(json_var))

# Processing
def process_stock_list(LIST_OF_DICTS):
	listings_data = []
	for listing in LIST_OF_DICTS:
		listing_info = {}

		listing_info['NAME'] = listing['instrument_info']['name']
		listing_info['TICKER'] = listing['instrument_info']['symbol']
		listing_info['ID'] = listing['instrument_info']['instrument_id']
		listing_info['ISIN'] = listing['instrument_info']['isin']
		"""if listing_info['ISIN'][:2] != "NO": # In case of non-norwegian instrument, thou some work - SAS NOK
			continue"""
		listing_info['MARKET_ID'] = listing['market_info']['market_id']
		listing_info['MARKET_IDENTIFIER'] = listing['market_info']['identifier']
		listing_info['HREF'] = "https://www.nordnet.no/market/stocks/" + str(listing_info['ID']) + "-" + listing_info['TICKER']

		# Array of dicts => in case of an update, it's the only thing that gets appended
		listing_info['PRICE_INFO'] = []
		listing_info['PRICE_INFO'].append(listing['price_info'])
		listing_info['KEY_RATIOS_INFO'] = listing['key_ratios_info']
		listing_info['HISTORICAL_RETURNS_INFO'] = listing['historical_returns_info']

		listings_data.append(listing_info)
	return listings_data
# TIME => DATETIME, UNIX, IDX, DATE_STRING
def process_stock_info(DICT_OF_LISTS_OF_DICTS, TIME="DATETIME"):
	time_series = {}

	for key in DICT_OF_LISTS_OF_DICTS:
		time_series[key] = {}
		time_series[key]['TIME'] = []
		time_series[key]['OPEN'] = []
		time_series[key]['HIGH'] = []
		time_series[key]['LOW'] = []
		time_series[key]['CLOSE'] = []
		time_series[key]['VOLUME'] = []

		list_of_dicts = DICT_OF_LISTS_OF_DICTS[key]
		counter = 0
		for dict_OHLCVT in list_of_dicts:
			if TIME == "DATETIME":
				time_series[key]['TIME'].append(datetime.utcfromtimestamp(dict_OHLCVT['time'] // 1000) + timedelta(hours=2))
			elif TIME == "UNIX":
				time_series[key]['TIME'].append(dict_OHLCVT['time'])
			elif TIME == "IDX":
				time_series[key]['TIME'].append(counter)
				counter += 1
			elif TIME == "DATE_STRING":
				time_series[key]['TIME'].append(datetime.utcfromtimestamp(dict_OHLCVT['time'] // 1000).strftime("%Y/%d/%d %H:%M:%S"))
			time_series[key]['OPEN'].append(dict_OHLCVT['open'])
			time_series[key]['HIGH'].append(dict_OHLCVT['high'])
			time_series[key]['LOW'].append(dict_OHLCVT['low'])
			time_series[key]['CLOSE'].append(dict_OHLCVT['last'])
			time_series[key]['VOLUME'].append(dict_OHLCVT['volume'])
		time_series[key]['DATASIZE'] = len(time_series[key]['TIME'])
	return time_series


class NordnetScraper:
	secs_remaining = 3600

	def __init__(self):
		self.session = requests.session()

	def login_sequence(self, DEBUG=False):
		sys.stdout.write("\n" + TextColors.WARNING + now_string() + " Logging in..." + TextColors.ENDC)
		sys.stdout.flush()

		self.session.headers.update({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})
		step_1 = self.session.get('https://classic.nordnet.no/mux/login/startNO.html?clearEndpoint=0&intent=next')
		if DEBUG:
			print_request_info(step_1, "GET LOGIN PAGE", PRINT_CONTENTS=False)

		step_2 = self.session.post('https://classic.nordnet.no/api/2/login/anonymous')
		self.session.headers.update({'ntag': step_2.headers['ntag']})
		if DEBUG:
			print_request_info(step_2, "POST LOGIN ANONYMOUS")

		payload = {'username': SECRETS.NORDNET_username, 'password': SECRETS.NORDNET_password}
		step_3 = self.session.post('https://classic.nordnet.no/api/2/authentication/basic/login', data=payload)
		self.session.headers.update({'ntag': step_3.headers['ntag']})
		if DEBUG:
			print_request_info(step_3, "POST LOGIN LOGIN")

		step_4 = self.session.get('https://classic.nordnet.no/api/2/customers/required_actions')
		self.session.headers.update({'ntag': step_4.headers['ntag']})
		if DEBUG:
			print_request_info(step_4, "GET LOGIN REQUIRED")

		step_5 = self.session.get('https://classic.nordnet.no/oauth2/authorize?client_id=NEXT&response_type=code&redirect_uri=https://www.nordnet.no/oauth2/')
		if DEBUG:
			print_request_info(step_5, "GET LOGIN AUTHORIZE", PRINT_CONTENTS=False)

		if step_5.ok:
			sys.stdout.write(TextColors.OKGREEN + "\r" + now_string() + " Logged in as " + payload['username'] + ".\n" + TextColors.ENDC)
		else:
			sys.stdout.write(TextColors.FAIL + "\r" + now_string() + " Could not log in.\n" + TextColors.ENDC)
			print_request_info(step_5, "GET LOGIN AUTHORIZE", PRINT_CONTENTS=False)
			self.session.__exit__()

		return step_5.request.headers

	# SORTED_BY => diff_pct, turnover
	def get_stock_list(self, SORTED_BY="turnover", DEBUG=False, DEBUG_CONTENTS=False):
		sys.stdout.write("\n" + TextColors.WARNING + now_string() + " Receiving instrument listings..." + TextColors.ENDC)
		sys.stdout.flush()

		listings_data = []
		self.session.headers.update(
			{'client-id': "NEXT", 'DNT': "1", 'Host': "www.nordnet.no", 'Referer': "https://www.nordnet.no/",
			 'Sec-Fetch-Dest': "empty", 'Sec-Fetch-Mode': "cors", 'Sec-Fetch-Site': "same-origin"})

		offset = [0, 100, 200]
		page = [1, 2, 3]

		for idx in range(3):
			get_stock_list_API = "https://www.nordnet.no/api/2/instrument_search/query/stocklist?sort_attribute=" + SORTED_BY + "&sort_order=desc&limit=100&offset=" + str(offset[idx]) + "&free_text_search=&apply_filters=exchange_country%3DNO%7Cexchange_list%3Dno%3Aose"
			stock_list_href = "https://www.nordnet.no/market/stocks?selectedTab=prices&sortField=" + SORTED_BY + "&sortOrder=desc&page=" + str(page[idx]) + "&exchangeCountry=NO&exchangeList=no%3Aose"

			self.session.headers.update({'x-nn-href': stock_list_href})

			get_stock_list = self.session.get(get_stock_list_API)
			stock_list_data = json.loads(get_stock_list.content.decode('UTF8'))['results']

			listings_data += stock_list_data

			if get_stock_list.ok:
				sys.stdout.write(
					TextColors.OKBLUE + "\r" + now_string() + " Received listings page " + str(idx + 1) + " out of 3." + TextColors.ENDC)
				sys.stdout.flush()
				if idx == 2:
					sys.stdout.write(
						TextColors.OKGREEN + "\r" + now_string() + " Received instrument listings sorted by " + SORTED_BY + "." + TextColors.ENDC)
			else:
				sys.stdout.write(TextColors.FAIL + "\r" + now_string() + " Could not get instrument listings.\n" + TextColors.ENDC)
				print_request_info(get_stock_list, "GET STOCK LIST", PRINT_CONTENTS=DEBUG_CONTENTS)
				self.logout()
				self.session.__exit__()

			if DEBUG:
				print_request_info(get_stock_list, "GET STOCK LIST", PRINT_CONTENTS=DEBUG_CONTENTS)
		return process_stock_list(listings_data)

	def login_check(self, DEBUG=False):
		login_check = self.session.get('https://www.nordnet.no/api/2/login')

		check_content = json.loads(login_check.content.decode('UTF8'))
		if (check_content['logged_in']) and check_content['session_type'] == 'authenticated':
			self.secs_remaining = check_content['remaining']
		else:
			print("Could not re-authenticate!")

		try:
			self.session.headers.update({'ntag': login_check.headers['ntag']})
		except KeyError:
			pass
		if DEBUG:
			print_request_info(login_check, "GET LOGIN CONFIRMATION")

	# ID_OPTION: ID, TICKER, NAME, ISIN
	def get_stock_info(self, STOCK_LIST, INSTRUMENT_ID, ID_OPTION='TICKER', PERIOD="0d", DEBUG=False):
		self.login_check()
		instrument_info = next((instrument for instrument in STOCK_LIST if instrument[ID_OPTION] == INSTRUMENT_ID), None)
		instrument_id = instrument_info['ID']
		instrument_ticker = instrument_info['TICKER']
		instrument_href = instrument_info['HREF']
		instrument_name = instrument_info['NAME']

		sys.stdout.write("\n" + TextColors.WARNING + now_string() + " Getting " + instrument_name + " (" + instrument_ticker + ") time series..." + TextColors.ENDC)
		sys.stdout.flush()

		self.session.headers.update(
			{'client-id': "NEXT", 'DNT': "1", 'Host': "www.nordnet.no", 'Referer': "https://www.nordnet.no/",
			 'Sec-Fetch-Dest': "empty", 'Sec-Fetch-Mode': "cors", 'Sec-Fetch-Site': "same-origin"})
		self.session.headers.update({'x-nn-href': instrument_href})

		back_date = calculate_back_days(PERIOD=PERIOD)

		API_url = "https://www.nordnet.no/api/2/instruments/historical/prices/" + str(instrument_id) + "?fields=open%2Chigh%2Clow%2Clast%2Cvolume&from=" + str(back_date)
		get_API_info = self.session.get(API_url)

		API_info = json.loads(get_API_info.content.decode('UTF8'))[0]['prices']

		if DEBUG:
			print_request_info(get_API_info, ("GET TIMESERIES " + str(instrument_ticker) + " from " + str(back_date)))

		if get_API_info.ok:
			sys.stdout.write(TextColors.OKGREEN + "\r" + now_string() + " Received " + instrument_name + " (" + instrument_ticker + ") time series." + TextColors.ENDC)
		else:
			sys.stdout.write(TextColors.FAIL + "\r" + now_string() + " Could not get " + instrument_name + " (" + instrument_ticker + ") time series." + TextColors.ENDC)

		self.login_check()
		return {instrument_ticker: API_info}

	# ID_OPTION: ID, TICKER, NAME, ISIN
	def get_multiple_stocks_info(self, STOCK_LIST, INSTRUMENT_IDS_LIST, ID_OPTION='TICKER', PERIOD="0d", DEBUG=False):
		stocks_data = {}
		for instrument in INSTRUMENT_IDS_LIST:
			instrument_info = self.get_stock_info(STOCK_LIST=STOCK_LIST, INSTRUMENT_ID=instrument, ID_OPTION=ID_OPTION, PERIOD=PERIOD, DEBUG=DEBUG)
			stocks_data.update(instrument_info)
		return stocks_data

	# ID_OPTION: ID, TICKER, NAME, ISIN
	def buy_sell_order(self, STOCK_LIST, ORDER, AMOUNT, INSTRUMENT_ID, ID_OPTION='TICKER', SAVE=True, VALID_UNTIL="TODAY", DEBUG=False, TEST=False):
		self.login_check()

		instrument_info = next((instrument for instrument in STOCK_LIST if instrument[ID_OPTION] == INSTRUMENT_ID), None)

		instrument_id = instrument_info['ID']
		instrument_ticker = instrument_info['TICKER']
		instrument_href = instrument_info['HREF']
		instrument_name = instrument_info['NAME']

		instrument_market_id = instrument_info['MARKET_ID']
		instrument_market_identifier = instrument_info['MARKET_IDENTIFIER']

		price = -99.0
		shares = -99
		amount = AMOUNT

		order_text = ""
		payload = ""

		if ORDER == "BUY":
			price = instrument_info['PRICE_INFO'][0]['ask']['price']

			order_text = " buy "

			shares = int(amount // price)

			payload = "order_type=LIMIT&price=" + str(price) + "&currency=NOK&identifier=" + str(instrument_market_identifier) + "&market_id=" + str(instrument_market_id) + "&side=buy&volume=" + str(shares) + "&valid_until=" + datetime.today().strftime("%Y-%m-%d")

		elif ORDER == "SELL":
			price = instrument_info['PRICE_INFO'][0]['bid']['price']

			order_text = " sell "

			shares = int(amount)
			amount = shares * price

			payload = "order_type=LIMIT&price=" + str(price) + "&currency=NOK&identifier=" + str(instrument_market_identifier) + "&market_id=" + str(instrument_market_id) + "&side=sell&volume=" + str(shares) + "&valid_until=" + datetime.today().strftime("%Y-%m-%d")

		sys.stdout.write(
			"\n" + TextColors.WARNING + now_string() + "Placing order to" + order_text + str(shares) + " " + instrument_name + " (" + instrument_ticker + ") shares for " + str(amount) + "NOK (" + str(price) + "NOK per share)..." + TextColors.ENDC)
		sys.stdout.flush()

		post_order = ''
		API_order_id = -1
		API_response = ''
		API_result = ''
		if not TEST:
			self.session.headers.update(
				{'client-id': "NEXT", 'DNT': "1", 'Host': "www.nordnet.no", 'Referer': "https://www.nordnet.no/",
				 'Sec-Fetch-Dest': "empty", 'Sec-Fetch-Mode': "cors", 'Sec-Fetch-Site': "same-origin"})
			self.session.headers.update({'x-nn-href': instrument_href + "/order/buy"})

			API_url = "https://www.nordnet.no/api/2/accounts/2/orders"
			post_order = self.session.post(API_url, data=payload)

			API_response = json.loads(post_order.content.decode('UTF8'))
			API_order_id = API_response['order_id']
			API_result = API_response['result_code']

		transaction_data = {'TIME': now_string(MILLIS=False), 'ID': instrument_id, 'TICKER': instrument_ticker,
		                    'NAME': instrument_name, 'HREF': instrument_href,
		                    'MARKET_ID': instrument_market_id, 'MARKET_IDENTIFIER': instrument_market_identifier,
		                    'SHARES': shares, 'SHARE_PRICE_NOK': price, 'AMOUNT_NOK': amount,
		                    'ORDER_ID': API_order_id}

		if not TEST:
			if DEBUG:
				print_request_info(post_order, ("POST ORDER" + str(instrument_ticker)))

			if API_result == "OK":
				sys.stdout.write(
					TextColors.OKGREEN + "\r" + now_string() + "Placed order to" + order_text + str(shares) + " " + instrument_name + " (" + instrument_ticker + ") shares for " + str(amount) + "NOK (" + str(price) + "NOK per share)." + TextColors.ENDC)
				if SAVE:
					update_transaction_file(transaction_data, ORDER=ORDER)
			else:
				sys.stdout.write(
					TextColors.FAIL + "\r" + now_string() + " Could not place order to" + order_text + str(shares) + " " + instrument_name + " (" + instrument_ticker + ") shares for " + str(amount) + "NOK (" + str(price) + "NOK per share)." + TextColors.ENDC)
				sys.stdout.write("\n" + str(API_response))

		self.login_check()
		return transaction_data

	def multiple_buy_sell_orders(self, STOCK_LIST, ORDERS, AMOUNTS, INSTRUMENT_IDS, ID_OPTION='TICKER', SAVE=True, VALID_UNTIL="TODAY", DEBUG=False, TEST=False):
		order = ''
		transactions_list = []
		for idx in range(len(INSTRUMENT_IDS)):
			instrument = INSTRUMENT_IDS[idx]
			amount = AMOUNTS[idx]
			if isinstance(ORDERS, str):
				order = ORDERS
			elif isinstance(ORDERS, list):
				order = ORDERS[idx]

			transaction = self.buy_sell_order(STOCK_LIST=STOCK_LIST, ORDER=order, AMOUNT=amount, INSTRUMENT_ID=instrument, ID_OPTION=ID_OPTION, SAVE=SAVE, VALID_UNTIL=VALID_UNTIL, DEBUG=DEBUG, TEST=TEST)
			transactions_list.append(transaction)
		return transactions_list

	def logout(self, DEBUG=False):
		sys.stdout.write("\n\n" + TextColors.WARNING + now_string() + " Logging out..." + TextColors.ENDC)
		sys.stdout.flush()
		sleep(1)
		step_1 = self.session.get('https://www.nordnet.no/api/2/login')

		if DEBUG:
			print_request_info(step_1, "GET LOGIN")

		step_2 = self.session.delete('https://www.nordnet.no/api/2/login')
		if DEBUG:
			print_request_info(step_2, "DELETE LOGIN")

		if step_2.ok:
			sys.stdout.write(TextColors.OKGREEN + "\r" + now_string() + " Logged out.\n" + TextColors.ENDC)
			self.session.__exit__()
		else:
			sleep(1)
			sys.stdout.write(TextColors.FAIL + "\r" + now_string() + "Could not log out.\n" + TextColors.ENDC)


def main(LISTINGS_SORTED_BY='turnover', SAVE_LISTINGS=False, **SERIES_PARAMS):
	"""
	:param LISTINGS_SORTED_BY: ``str``:
		'diff_pct', 'turnover_volume' 'turnover', 'spread_pct', etc.

	:param SAVE_LISTINGS: ``bool``:
		Set to True to save listings to file.

	:param SERIES_PARAMS:

	:keyword GET_SERIES: ``str``:
		'NONE', 'SINGLE' or 'MULTIPLE'.

	:keyword TICKER: ``str`` or ``list``:
		'SAS NOK', etc or ['SAS NOK', 'PGS', ...], etc.

	:keyword PERIOD: ``str`` len(2):
		'0d', '1d', '6d', '1w', '1m', '3m', '1y', etc. '9y' max.

	:keyword TIME_TYPE: ``str``:
		'IDX', 'DATETIME', 'UNIX' or 'DATE_STRING'.

	:return: time series if enabled, else returns listings.
	"""

	scraper = NordnetScraper()
	scraper.login_sequence()

	instrument_listings = scraper.get_stock_list(SORTED_BY=LISTINGS_SORTED_BY)
	if SAVE_LISTINGS:
		save_instrument_listings(instrument_listings)

	time_series = False
	instrument_time_series = ''
	if 'GET_SERIES' in SERIES_PARAMS:
		if SERIES_PARAMS['GET_SERIES'] == 'NONE':
			pass
		else:
			if 'TICKER' not in SERIES_PARAMS:
				scraper.logout()
				raise KeyError("Must specify 'TICKER' argument to get instrument info.")
			elif 'PERIOD' not in SERIES_PARAMS:
				SERIES_PARAMS['PERIOD'] = '1d'
			else:
				if SERIES_PARAMS['GET_SERIES'] == 'SINGLE':
					time_series = True
					instrument_time_series = scraper.get_stock_info(instrument_listings, SERIES_PARAMS['TICKER'], 'TICKER', PERIOD=SERIES_PARAMS['PERIOD'])
				elif SERIES_PARAMS['GET_SERIES'] == 'MULTIPLE':
					if not isinstance(SERIES_PARAMS['TICKER'], list):
						scraper.logout()
						raise ValueError("'TICKER' parameter must be list to get multiple time series.")
					time_series = True
					instrument_time_series = scraper.get_multiple_stocks_info(instrument_listings, SERIES_PARAMS['TICKER'], 'TICKER', PERIOD=SERIES_PARAMS['PERIOD'])
				else:
					scraper.logout()
					raise ValueError(SERIES_PARAMS['GET_SERIES'] + " value doesn't exist as a series argument.")

				if 'TIME_TYPE' not in SERIES_PARAMS:
					SERIES_PARAMS['TIME_TYPE'] = 'IDX'

				instrument_time_series = (process_stock_info(instrument_time_series, TIME=SERIES_PARAMS['TIME_TYPE']))

	#scraper.buy_sell_order('BUY', 10, 'IOX')

	scraper.logout()

	if time_series:
		return instrument_time_series
	else:
		return instrument_listings


#main(GET_SERIES='NONE', TICKER='ENDUR', PERIOD='0d')