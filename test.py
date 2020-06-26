from Scrapers import NordnetScraper
from Controllers import RelevantStocksFilter, TAlibWrapper, BankAccounts
from Models import TIModels

account = BankAccounts.Bank(1000)
account.import_transaction_file()

scraper = NordnetScraper.NordnetScraper()
scraper.login_sequence()
listings = scraper.get_stock_list()

relevant_listings = RelevantStocksFilter.find_relevant_stocks(listings, DIFF_PCT='>0.0', EPS='>0.0', TURNOVER_VOLUME='>10000')
print(len(relevant_listings))
relevant_listings = relevant_listings[:15]


ticker_list = [listing['TICKER'] for listing in relevant_listings]
data_series = scraper.get_multiple_stocks_info(listings, ticker_list, PERIOD='1d')
data_series = NordnetScraper.process_stock_info(data_series)

rsi_trigg_mem = {}
macd_trigg_mem = {}
bbands_trigg_mem = {}
bbands_roc_trigg_mem = {}
for name in data_series:
	rsi_trigg_mem[name] = 50
	macd_trigg_mem[name] = {'BUY': -2, 'SELL': 2}
	bbands_trigg_mem[name] = []
	bbands_roc_trigg_mem[name] = []

print("\n")
for data_set in data_series:
	time_series = data_series[data_set]['TIME']
	open_series = data_series[data_set]['OPEN']
	high_series = data_series[data_set]['HIGH']
	low_series = data_series[data_set]['LOW']
	close_series = data_series[data_set]['CLOSE']
	volume_series = data_series[data_set]['VOLUME']

	hours = 8
	cut_data = TAlibWrapper.SERIES_CUTOFF(time_series, close_series, N_HOURS=hours)
	TIME_cut = cut_data[0]
	CLOSE_cut = cut_data[1]
	HIGH_cut = TAlibWrapper.SERIES_CUTOFF(time_series, high_series, N_HOURS=hours)[1]
	LOW_cut = TAlibWrapper.SERIES_CUTOFF(time_series, low_series, N_HOURS=hours)[1]

	print(data_set)
	rsi_trigg = TIModels.RSI_trigger(CLOSE_cut, rsi_trigg_mem[data_set], DEBUG=True)
	macd_trigg = TIModels.MACD_signal_normalized_trigger(CLOSE_cut, macd_trigg_mem[data_set], DEBUG=True)
	bbands_trigg = TIModels.BBANDS_trigger(CLOSE_cut, bbands_trigg_mem[data_set], DEBUG=True)
	bbands_trigg_roc = TIModels.BBANDS_ROC_trigger(CLOSE_cut, bbands_roc_trigg_mem[data_set], DEBUG=True)

"""listings = scraper.get_stock_list()
#use_money = account.money // len(relevant_listings)
transactions = scraper.multiple_buy_sell_orders(listings, 'BUY', 100, ticker_list, TEST=True)

for order in transactions:
    account.bought_shares(order)

print(account.shares_owned)
print(account.shares_bought)
print(account.shares_sold)
"""
scraper.logout()