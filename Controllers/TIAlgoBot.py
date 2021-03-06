from Scrapers import NordnetScraper
from Controllers import RelevantStocksFilter, TAlibWrapper, BankAccounts
from Scripts.TextColors import TextColors
import sys
from Models import TIModels

class TIAlgoBot:
	instrument_listings = []
	relevant_listings = []
	relevant_tickers = []
	exiled_tickers = []
	relevant_tickers_settings = {}

	tick_series = {}

	RSI_mem = {}
	MACD_mem = {}
	BBANDS_mem = {}
	BBANDS_ROC_mem = {}

	# Models => RSI, MACD, BBANDS_ROC, BBANDS
	def __init__(self, money=1000, **models):
		self.account = BankAccounts.Bank(money)
		self.scraper = NordnetScraper.NordnetScraper()
		self.models = models

	def login(self):
		self.scraper = NordnetScraper.NordnetScraper()
		self.scraper.login_sequence()

	def logout(self):
		self.scraper.logout()

	def apply_models(self):
		self.hey = 1

	def update_instrument_listings(self, SORTED_BY='turnover'):
		self.instrument_listings = self.scraper.get_stock_list(SORTED_BY=SORTED_BY)

	def get_relevant_instruments(self, ONLY_NEW=True, SAVE=False, NUMBER_OF_RELEVANT_INSTRUMENTS=5, **RELEVANT_INSTRUMENTS_PARAMS):
		all_relevant_listings = RelevantStocksFilter.find_relevant_stocks(self.instrument_listings,
		                                                                   SAVE=SAVE,
		                                                                   **RELEVANT_INSTRUMENTS_PARAMS)
		if ONLY_NEW:
			listings_left = NUMBER_OF_RELEVANT_INSTRUMENTS
			new_listings = []
			for i in range(len(all_relevant_listings)):
				listing = all_relevant_listings[i]
				if listing['TICKER'] not in self.relevant_tickers:
					new_listings.append(listing)
					listings_left -= 1
				if listings_left <= 0:
					break
			self.relevant_listings = new_listings
			self.relevant_tickers = [listing['TICKER'] for listing in self.relevant_listings]
		else:
			self.relevant_listings = all_relevant_listings[:NUMBER_OF_RELEVANT_INSTRUMENTS]
			self.relevant_tickers = [listing['TICKER'] for listing in self.relevant_listings]

	def append_relevant_instruments(self, SAVE=False, TOTAL_NUMBER_OF_RELEVANT_LISTINGS=5, **RELEVANT_INSTRUMENTS_PARAMS):
		number_of_new_listings = TOTAL_NUMBER_OF_RELEVANT_LISTINGS - len(self.relevant_tickers)
		if number_of_new_listings <= 0:
			sys.stdout.write(
				f"\n{TextColors.FAIL}{NordnetScraper.now_string()} There are already {TOTAL_NUMBER_OF_RELEVANT_LISTINGS} instruments or more in relevant instruments list.{TextColors.ENDC}")
			return

		all_relevant_listings = RelevantStocksFilter.find_relevant_stocks(self.instrument_listings,
		                                                                  SAVE=SAVE,
		                                                                  **RELEVANT_INSTRUMENTS_PARAMS)

		for listing in all_relevant_listings:
			ticker = listing['TICKER']
			if ticker not in self.relevant_tickers and ticker not in self.exiled_tickers:
				self.relevant_listings.append(listing)
				self.relevant_tickers.append(ticker)
				number_of_new_listings -= 1

			if number_of_new_listings <= 0:
				break

	def delete_relevant_instruments(self, *TICKERS):
		for ticker in TICKERS:
			listing_index = next((i for i, item in enumerate(self.relevant_listings) if item["TICKER"] == ticker), None)
			if listing_index is None:
				sys.stdout.write(f"\n{TextColors.FAIL}{NordnetScraper.now_string()} {ticker} was not found in relevant instrument list.{TextColors.ENDC}")
				continue

			self.exiled_tickers.append(ticker)
			del self.relevant_listings[listing_index]
			self.relevant_tickers.remove(ticker)

	def startup(self, SORTED_BY='turnover', NUMBER_OF_RELEVANT_INSTRUMENTS=5, SAVE=False, **RELEVANT_INSTRUMENTS_PARAMS):
		self.account.import_transaction_file()
		self.scraper.login_sequence()

		self.instrument_listings = self.scraper.get_stock_list(SORTED_BY=SORTED_BY)

		all_relevant_listings = RelevantStocksFilter.find_relevant_stocks(self.instrument_listings,
		                                                                  SAVE=SAVE,
		                                                                  **RELEVANT_INSTRUMENTS_PARAMS)
		self.relevant_tickers_settings.update(**RELEVANT_INSTRUMENTS_PARAMS)
		self.relevant_listings = all_relevant_listings[:NUMBER_OF_RELEVANT_INSTRUMENTS]
		self.relevant_tickers = [listing['TICKER'] for listing in self.relevant_listings]

	def get_tick_data(self, TICKER_LIST, PERIOD='1d', HOURS_BACK=8):
		data_series = self.scraper.get_multiple_stocks_info(self.instrument_listings, TICKER_LIST, PERIOD=PERIOD)
		data_series = NordnetScraper.process_stock_info(data_series, TIME='DATETIME')

		self.tick_series = {}
		if HOURS_BACK is None:
			self.tick_series = data_series
			return self.tick_series

		elif isinstance(HOURS_BACK, int):
			for ticker in data_series:
				time_series = data_series[ticker]['TIME']
				open_series = data_series[ticker]['OPEN']
				high_series = data_series[ticker]['HIGH']
				low_series = data_series[ticker]['LOW']
				close_series = data_series[ticker]['CLOSE']
				volume_series = data_series[ticker]['VOLUME']
				datasize = data_series[ticker]['DATASIZE']
				if datasize < 25:
					self.delete_relevant_instruments(ticker)
					self.exiled_tickers.append(ticker)

					continue

				cut_data = TAlibWrapper.SERIES_CUTOFF(time_series, open_series, N_HOURS=HOURS_BACK)
				TIME_cut = cut_data[0]
				OPEN_cut = cut_data[1]
				HIGH_cut = TAlibWrapper.SERIES_CUTOFF(time_series, high_series, N_HOURS=HOURS_BACK)[1]
				LOW_cut = TAlibWrapper.SERIES_CUTOFF(time_series, low_series, N_HOURS=HOURS_BACK)[1]
				CLOSE_cut = TAlibWrapper.SERIES_CUTOFF(time_series, close_series, N_HOURS=HOURS_BACK)[1]
				VOLUME_cut = TAlibWrapper.SERIES_CUTOFF(time_series, volume_series, N_HOURS=HOURS_BACK)[1]
				DATASIZE_cut = len(TIME_cut)

				self.tick_series[ticker] = {'TIME': TIME_cut,
				                            'OPEN': OPEN_cut,
				                            'HIGH': HIGH_cut,
				                            'LOW': LOW_cut,
				                            'CLOSE': CLOSE_cut,
				                            'VOLUME': VOLUME_cut,
				                            'DATASIZE': DATASIZE_cut}
			return self.tick_series
		else:
			self.logout()
			raise ValueError("Param 'HOURS_BACK' has to be either Nonetype 'None' or an integer up to 14.")

	def TIModels_triggers(self):
		for ticker in self.tick_series:
			if 'RSI' in self.models:
				if ticker not in self.RSI_mem:
					self.RSI_mem[ticker] = 50
			if 'MACD' in self.models:
				if ticker not in self.MACD_mem:
					self.MACD_mem[ticker] = {'BUY': -2, 'SELL': 2}
			if 'BBANDS' in self.models:
				if ticker not in self.BBANDS_mem:
					self.BBANDS_mem[ticker] = []
			if 'BBANDS_ROC' in self.models:
				if ticker not in self.BBANDS_ROC_mem:
					self.BBANDS_ROC_mem[ticker] = []

		for ticker in self.tick_series:
			close_series = self.tick_series[ticker]['CLOSE']
			if 'RSI' in self.models:
				RSI_trigger = TIModels.RSI_trigger(close_series, self.RSI_mem[ticker], INDEXES_BACK=self.models['RSI'], DEBUG=True)
			if 'MACD' in self.models:
				MACD_trigger = TIModels.MACD_signal_normalized_trigger(close_series, self.MACD_mem[ticker], INDEXES_BACK=self.models['MACD'], DEBUG=True)
			if 'BBANDS' in self.models:
				BBANDS_trigger = TIModels.BBANDS_trigger(close_series, self.BBANDS_mem[ticker], INDEXES_BACK=self.models['BBANDS'], DEBUG=True)
			if 'BBANDS_ROC' in self.models:
				BBANDS_ROC_trigger = TIModels.BBANDS_ROC_trigger(close_series, self.BBANDS_ROC_mem[ticker], INDEXES_BACK=self.models['BBANDS_ROC'], DEBUG=True)
			sys.stdout.write(
				f"\n{TextColors.OKGREEN}{NordnetScraper.now_string()} Applied {self.models} models to {ticker}.{TextColors.ENDC}\n")
bot = TIAlgoBot(1000, RSI=2, MACD=5, BBANDS=5)
bot.startup(EPS='>0.0', YIELD_1W='>0.0', YIELD_1D='>0.0', CLOSE='<100')
bot.get_tick_data(bot.relevant_tickers)
bot.TIModels_triggers()

bot.logout()