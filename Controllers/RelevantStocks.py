import json
from datetime import datetime


def check_if_value_under_limit(VALUE, LIMIT):
	if VALUE is None:
		return True
	elif VALUE < LIMIT:
		return True
	else:
		return False


with open('C:\\Users\\theba\\PycharmProjects\\StockTradingBot\\_LogsListings\\listings_19-06-2020_09-22-07.json', 'r') as file:
	instrument_list = json.loads(file.read())

relevant_instruments = []
for instrument in instrument_list:
	try:
		eps = instrument['KEY_RATIOS_INFO']['eps']
	except KeyError:
		eps = None

	try:
		yield_1w = instrument['HISTORICAL_RETURNS_INFO']['yield_1w']
	except KeyError:
		yield_1w = None

	try:
		yield_1d = instrument['HISTORICAL_RETURNS_INFO']['yield_1d']
	except KeyError:
		yield_1d = None

	try:
		diff_pct = instrument['PRICE_INFO'][0]['diff_pct']
	except KeyError:
		diff_pct = None

	if check_if_value_under_limit(eps, 0.0):
		continue
	if check_if_value_under_limit(yield_1d, 0.0):
		continue
	if check_if_value_under_limit(yield_1w, 0.0):
		continue
	if check_if_value_under_limit(diff_pct, 1.0):
		continue
	relevant_instruments.append(instrument)
relevant_instruments = sorted(relevant_instruments, key = lambda i: i['PRICE_INFO'][0]['spread_pct'])
print(relevant_instruments)
print(len(relevant_instruments))