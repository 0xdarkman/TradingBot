from Controllers.RelevantStocksFilter import *
from Scrapers import NordnetScraper

money_total = 995

def startup_get_stocks():
	scraper = NordnetScraper.NordnetScraper()
	scraper.login_sequence()

	instrument_list = scraper.get_stock_list(SORTED_BY='turnover')
	relevant_stocks = find_relevant_stocks(instrument_list, SAVE=True, YIELD_1W='>0.0', YIELD_1D='>0.0', DIFF_PCT='<10.0')
	return relevant_stocks
