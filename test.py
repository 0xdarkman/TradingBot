from Scrapers import NordnetScraper
from Controllers import RelevantStocksFilter, TAlibWrapper, BankAccounts

account = BankAccounts.Bank(1000)
account.import_transaction_file()

scraper = NordnetScraper.NordnetScraper()
scraper.login_sequence()
listings = scraper.get_stock_list()

relevant_listings = RelevantStocksFilter.find_relevant_stocks(listings, DIFF_PCT='>5.0')
relevant_listings = relevant_listings[:5]

ticker_list = [listing['TICKER'] for listing in relevant_listings]
time_series = scraper.get_multiple_stocks_info(listings, ticker_list, PERIOD='1d')
time_series = NordnetScraper.process_stock_info(time_series)




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