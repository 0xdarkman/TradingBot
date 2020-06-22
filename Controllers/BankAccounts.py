# TODO: Add separate accounts for each share, also a way to add and remove share accounts, separate money,
#  add/remove money to/from accounts from trades

# TODO: Compare money sold to bought with order ids instead of just comparing sold to owned info
class Bank:
	shares_owned = {}
	shares_bought = []
	shares_sold = []
	"""{'TIME': now_string(MILLIS=False), 'ID': instrument_id, 'TICKER': instrument_ticker,
	 'NAME': instrument_name, 'HREF': instrument_href,
	 'MARKET_ID': instrument_market_id, 'MARKET_IDENTIFIER': instrument_market_identifier,
	 'SHARES': shares, 'SHARE_PRICE_NOK': price, 'AMOUNT_NOK': amount,
	 'ORDER_ID': API_order_id}"""

	def __init__(self, money):
		self.money_total = money

	def add_money(self, AMOUNT):
		self.money_total += AMOUNT
		return self.money_total

	def take_money(self, AMOUNT):
		self.money_total -= AMOUNT
		return self.money_total

	def get_money(self):
		return self.money_total

	def bought_shares(self, BUY_ORDER_DICT):
		ticker = BUY_ORDER_DICT['TICKER']

		if ticker not in self.shares_owned:
			self.shares_owned[ticker] = BUY_ORDER_DICT
		else:
			self.shares_owned[ticker]['TIME'] = BUY_ORDER_DICT['TIME']
			self.shares_owned[ticker]['SHARES'] += BUY_ORDER_DICT['SHARES']
			self.shares_owned[ticker]['SHARE_PRICE_NOK'] = BUY_ORDER_DICT['SHARE_PRICE_NOK']
			self.shares_owned[ticker]['AMOUNT_NOK'] = self.shares_owned[ticker]['SHARES'] * self.shares_owned[ticker]['SHARE_PRICE_NOK']
			self.shares_owned[ticker]['ORDER_ID'] = BUY_ORDER_DICT['ORDER_ID']
		self.shares_bought.append(BUY_ORDER_DICT)

	def sold_shares(self, SELL_ORDER_DICT):
		transaction_dict = SELL_ORDER_DICT
		ticker = transaction_dict['TICKER']

		transaction_dict['DIFF'] = transaction_dict['AMOUNT_NOK'] - self.shares_owned[ticker]['AMOUNT_NOK']
		transaction_dict['DIFF_PCT'] = (transaction_dict['AMOUNT_NOK'] / self.shares_owned[ticker]['AMOUNT_NOK'] - 1) * 100

		self.shares_sold.append(transaction_dict)

		if transaction_dict['SHARES'] == self.shares_owned[ticker]['SHARES']:
			del self.shares_owned[ticker]
		else:
			self.shares_owned[ticker]['TIME'] = transaction_dict['TIME']
			self.shares_owned[ticker]['SHARES'] += transaction_dict['SHARES']
			self.shares_owned[ticker]['SHARE_PRICE_NOK'] = transaction_dict['SHARE_PRICE_NOK']
			self.shares_owned[ticker]['AMOUNT_NOK'] = self.shares_owned[ticker]['SHARES'] * self.shares_owned[ticker]['SHARE_PRICE_NOK']
			self.shares_owned[ticker]['ORDER_ID'] = transaction_dict['ORDER_ID']

