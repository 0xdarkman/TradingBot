import json
from datetime import datetime


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
		self.money = money

	def add_money(self, AMOUNT):
		self.money += AMOUNT
		return self.money

	def take_money(self, AMOUNT):
		self.money -= AMOUNT
		return self.money

	def get_money(self, PRINT=True):
		if PRINT:
			print(self.money)
		return self.money

	def update_transaction_file(self):
		json_var = {'BOUGHT': self.shares_bought,
		            'SOLD': self.shares_sold,
		            'OWNED': self.shares_owned}

		with open('C:\\Users\\theba\\PycharmProjects\\StockTradingBot\\_LogsTransactions\\shares_' +
		          datetime.now().strftime("%d-%m-%Y") + '.json', 'w') as file:
			file.write(json.dumps(json_var))

	def import_transaction_file(self):
		json_var = {}
		try:
			with open('C:\\Users\\theba\\PycharmProjects\\StockTradingBot\\_LogsTransactions\\shares_' +
			          datetime.now().strftime("%d-%m-%Y") + '.json', 'r') as file:
				json_var = json.loads(file.read())
			self.shares_bought = json_var['BOUGHT']
			self.shares_sold = json_var['SOLD']
			self.shares_owned = json_var['OWNED']

			money_used = 0
			for share in self.shares_owned:
				money_used += self.shares_owned[share]['AMOUNT_NOK']
			self.money -= money_used

			return True
		except FileNotFoundError:
			print("A log file from today wasn't found.")
			return False

	def bought_shares(self, BUY_ORDER_DICT):
		ticker = BUY_ORDER_DICT['TICKER']

		self.take_money(BUY_ORDER_DICT['AMOUNT_NOK'])
		if ticker not in self.shares_owned:
			self.shares_owned[ticker] = BUY_ORDER_DICT
		else:
			self.shares_owned[ticker]['TIME'] = BUY_ORDER_DICT['TIME']
			self.shares_owned[ticker]['SHARES'] += BUY_ORDER_DICT['SHARES']
			self.shares_owned[ticker]['SHARE_PRICE_NOK'] = BUY_ORDER_DICT['SHARE_PRICE_NOK']
			self.shares_owned[ticker]['AMOUNT_NOK'] = self.shares_owned[ticker]['SHARES'] * self.shares_owned[ticker][
				'SHARE_PRICE_NOK']
			self.shares_owned[ticker]['ORDER_ID'] = BUY_ORDER_DICT['ORDER_ID']
		self.shares_bought.append(BUY_ORDER_DICT)

		self.update_transaction_file()

	def sold_shares(self, SELL_ORDER_DICT):
		transaction_dict = SELL_ORDER_DICT
		ticker = transaction_dict['TICKER']

		transaction_dict['DIFF'] = transaction_dict['AMOUNT_NOK'] - self.shares_owned[ticker]['AMOUNT_NOK']
		transaction_dict['DIFF_PCT'] = (transaction_dict['AMOUNT_NOK'] / self.shares_owned[ticker][
			'AMOUNT_NOK'] - 1) * 100

		self.shares_sold.append(transaction_dict)

		if transaction_dict['SHARES'] == self.shares_owned[ticker]['SHARES']:
			del self.shares_owned[ticker]
		else:
			self.shares_owned[ticker]['TIME'] = transaction_dict['TIME']
			self.shares_owned[ticker]['SHARES'] += transaction_dict['SHARES']
			self.shares_owned[ticker]['SHARE_PRICE_NOK'] = transaction_dict['SHARE_PRICE_NOK']
			self.shares_owned[ticker]['AMOUNT_NOK'] = self.shares_owned[ticker]['SHARES'] * self.shares_owned[ticker][
				'SHARE_PRICE_NOK']
			self.shares_owned[ticker]['ORDER_ID'] = transaction_dict['ORDER_ID']

		self.update_transaction_file()

