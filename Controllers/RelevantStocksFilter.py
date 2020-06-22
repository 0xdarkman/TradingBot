import json
from datetime import datetime
from Scrapers.NordnetScraper import save_instrument_listings

"""with open('C:\\Users\\theba\\PycharmProjects\\StockTradingBot\\_LogsListings\\listings_19-06-2020_09-22-07.json', 'r') as file:
	instrument_list = json.loads(file.read())"""

def find_relevant_stocks(STOCK_LIST, SAVE=False, **SORT_ARGS):
	"""
	:param STOCK_LIST:
	:param SAVE:
	:param SORT_BY:
	:param SORT_ARGS: SORT_ARG='<(float)', '>(float)'
	:return:
	"""
	relevant_instruments = []
	for instrument in STOCK_LIST:
		is_relevant = True
		instrument_dict = instrument

		info_dictionary = {}
		default_var = -999
		instrument_dict['KEY_RATIOS_INFO'].setdefault('ps', default_var)
		instrument_dict['KEY_RATIOS_INFO'].setdefault('eps', default_var)
		instrument_dict['KEY_RATIOS_INFO'].setdefault('pb', default_var)
		instrument_dict['KEY_RATIOS_INFO'].setdefault('pe', default_var)
		instrument_dict['HISTORICAL_RETURNS_INFO'].setdefault('yield_1d', default_var)
		instrument_dict['HISTORICAL_RETURNS_INFO'].setdefault('yield_1w', default_var)
		instrument_dict['HISTORICAL_RETURNS_INFO'].setdefault('yield_1m', default_var)
		instrument_dict['HISTORICAL_RETURNS_INFO'].setdefault('yield_3m', default_var)
		instrument_dict['HISTORICAL_RETURNS_INFO'].setdefault('yield_ytd', default_var)
		instrument_dict['HISTORICAL_RETURNS_INFO'].setdefault('yield_1y', default_var)
		instrument_dict['PRICE_INFO'][0].setdefault('diff', {'diff': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('diff_pct', default_var)
		instrument_dict['PRICE_INFO'][0].setdefault('last', {'price': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('open', {'price': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('close', {'price': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('high', {'price': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('low', {'price': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('bid', {'price': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('ask', {'price': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('turnover', default_var)
		instrument_dict['PRICE_INFO'][0].setdefault('turnover_normalized', default_var)
		instrument_dict['PRICE_INFO'][0].setdefault('turnover_volume', default_var)
		instrument_dict['PRICE_INFO'][0].setdefault('bid_volume', default_var)
		instrument_dict['PRICE_INFO'][0].setdefault('ask_volume', default_var)
		instrument_dict['PRICE_INFO'][0].setdefault('spread', {'price': default_var})
		instrument_dict['PRICE_INFO'][0].setdefault('spread_pct', default_var)

		info_dictionary = {'LAST': instrument_dict['PRICE_INFO'][0]['last']['price'],
		                   'OPEN': instrument_dict['PRICE_INFO'][0]['open']['price'],
		                   'CLOSE': instrument_dict['PRICE_INFO'][0]['close']['price'],
		                   'TURNOVER': instrument_dict['PRICE_INFO'][0]['turnover'],
		                   'TURNOVER_NORMALIZED': instrument_dict['PRICE_INFO'][0]['turnover_normalized'],
		                   'TURNOVER_VOLUME': instrument_dict['PRICE_INFO'][0]['turnover_normalized'],
		                   'SELL_PRICE': instrument_dict['PRICE_INFO'][0]['bid']['price'],
		                   'BUY_PRICE': instrument_dict['PRICE_INFO'][0]['ask']['price'],
		                   'SELL_VOLUME': instrument_dict['PRICE_INFO'][0]['bid_volume'],
		                   'BUY_VOLUME': instrument_dict['PRICE_INFO'][0]['ask_volume'],
		                   'HIGH': instrument_dict['PRICE_INFO'][0]['high']['price'],
		                   'LOW': instrument_dict['PRICE_INFO'][0]['low']['price'],
		                   'DIFF': instrument_dict['PRICE_INFO'][0]['diff']['diff'],
		                   'DIFF_PCT': instrument_dict['PRICE_INFO'][0]['diff_pct'],
		                   'SPREAD': instrument_dict['PRICE_INFO'][0]['spread']['price'],
		                   'SPREAD_PCT': instrument_dict['PRICE_INFO'][0]['spread_pct'],
		                   'PS': instrument_dict['KEY_RATIOS_INFO']['ps'],
		                   'EPS': instrument_dict['KEY_RATIOS_INFO']['eps'],
		                   'PB': instrument_dict['KEY_RATIOS_INFO']['pb'],
		                   'PE': instrument_dict['KEY_RATIOS_INFO']['pe'],
		                   'YIELD_1D': instrument_dict['HISTORICAL_RETURNS_INFO']['yield_1d'],
		                   'YIELD_1W': instrument_dict['HISTORICAL_RETURNS_INFO']['yield_1w'],
		                   'YIELD_1M': instrument_dict['HISTORICAL_RETURNS_INFO']['yield_1m'],
		                   'YIELD_3M': instrument_dict['HISTORICAL_RETURNS_INFO']['yield_3m'],
		                   'YIELD_YTD': instrument_dict['HISTORICAL_RETURNS_INFO']['yield_ytd'],
		                   'YIELD_1Y': instrument_dict['HISTORICAL_RETURNS_INFO']['yield_1y']}

		for sort_key in SORT_ARGS:
			less_greater_than = SORT_ARGS[sort_key][0]
			limit_value = float(SORT_ARGS[sort_key][1:])
			check_value = info_dictionary[sort_key]

			if check_value == default_var:
				is_relevant = False

			if less_greater_than == '<':
				try:
					if check_value >= limit_value:  # if indicator value is bigger than set limit, dont append it
						is_relevant = False
				except KeyError:
					pass

			elif less_greater_than == '>':  # if indicator value is smaller than set limit, dont append it
				try:
					if check_value <= limit_value:
						is_relevant = False
				except KeyError:
					pass
			else:
				raise ValueError("First character of a 'SORT_ARGS' paramater value must be either '<' or '>'.")

			#print(f'Is {sort_key}={check_value} {less_greater_than} {limit_value}? {is_relevant}')
			if not is_relevant:
				break

		if is_relevant:
			relevant_instruments.append(instrument_dict)

	if SAVE:
		name = ''
		for sort_key in SORT_ARGS:
			name += sort_key + SORT_ARGS[sort_key] + '&'
		name = name.replace('.', ',').replace('<', 'lsthn').replace('>', 'mrthn')
		name = name[:-1]
		name += '%'
		save_instrument_listings(relevant_instruments, ('listings%' + name))
