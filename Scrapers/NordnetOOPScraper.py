import requests
import SECRETS
import json
from time import sleep


def print_request_info(REQUEST_VARIABLE, REQUEST_DESCRIPTION, PRINT_CONTENTS=True):
	if PRINT_CONTENTS:
		print(str(REQUEST_DESCRIPTION), "\n\n",
		      "Status Code:\n", REQUEST_VARIABLE.status_code, "\n\n",
		      "Req Headers:\n", REQUEST_VARIABLE.request.headers, "\n\n",
		      "Res Headers:\n", REQUEST_VARIABLE.headers, "\n\n",
		      "Res Cookies:\n", REQUEST_VARIABLE.cookies, "\n\n",
		      "Res Content:\n", REQUEST_VARIABLE.content,
		      "\n\n\n")
	else:
		print(str(REQUEST_DESCRIPTION), "\n\n",
		      "Status Code:\n", REQUEST_VARIABLE.status_code, "\n\n",
		      "Req Headers:\n", REQUEST_VARIABLE.request.headers, "\n\n",
		      "Res Headers:\n", REQUEST_VARIABLE.headers, "\n\n",
		      "Res Cookies:\n", REQUEST_VARIABLE.cookies,
		      "\n\n\n")


class NordnetScraper:
	payload = {'username': SECRETS.NORDNET_username, 'password': SECRETS.NORDNET_password}

	def __init__(self):
		self.session = requests.session()

	def login_sequence(self, DEBUG=False):
		self.session.headers.update({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})
		step_1 = self.session.get('https://classic.nordnet.no/mux/login/startNO.html?clearEndpoint=0&intent=next')
		if DEBUG:
			print_request_info(step_1, "GET LOGIN PAGE", PRINT_CONTENTS=False)

		step_2 = self.session.post('https://classic.nordnet.no/api/2/login/anonymous')
		self.session.headers.update({'ntag': step_2.headers['ntag']})
		if DEBUG:
			print_request_info(step_2, "POST LOGIN ANONYMOUS")

		step_3 = self.session.post('https://classic.nordnet.no/api/2/authentication/basic/login', data=self.payload)
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

		return step_5.request.headers

	def get_stock_list(self, DEBUG=False, DEBUG_CONTENTS=False):
		listings_data = []
		self.session.headers.update(
			{'client-id': "NEXT", 'DNT': "1", 'Host': "www.nordnet.no", 'Referer': "https://www.nordnet.no/",
			 'Sec-Fetch-Dest': "empty", 'Sec-Fetch-Mode': "cors", 'Sec-Fetch-Site': "same-origin"})

		offset = [0, 100, 200]
		page = [1, 2, 3]

		for idx in range(3):
			get_stock_list_API = "https://www.nordnet.no/api/2/instrument_search/query/stocklist?sort_attribute=turnover_normalized&sort_order=desc&limit=100&offset=" + str(offset[idx]) + "&free_text_search=&apply_filters=exchange_country%3DNO%7Cexchange_list%3Dno%3Aose"
			stock_list_href = "https://www.nordnet.no/market/stocks?selectedTab=prices&sortField=turnover&sortOrder=desc&page=" + str(page[idx]) + "&exchangeCountry=NO&exchangeList=no%3Aose"

			self.session.headers.update({'x-nn-href': stock_list_href})

			stock_list = self.session.get(get_stock_list_API)
			stock_list_data = json.loads(stock_list.content.decode('UTF8'))['results']

			listings_data += stock_list_data
			if DEBUG:
				print_request_info(stock_list, "GET STOCK LIST", PRINT_CONTENTS=DEBUG_CONTENTS)

		return listings_data

	def logout(self, DEBUG=False):
		print("\nLogging Out...", end="")
		sleep(3)

		step_1 = self.session.get('https://www.nordnet.no/api/2/login')
		if DEBUG:
			print_request_info(step_1, "GET LOGIN")

		step_2 = self.session.delete('https://www.nordnet.no/api/2/login')
		if DEBUG:
			print_request_info(step_2, "DELETE LOGIN")

		if step_2.ok:
			self.session.__exit__()
			print("Logged out successfully.")
		else:
			print("Could not log out.")


scraper = NordnetScraper()
scraper.login_sequence()
stock_data = scraper.get_stock_list()
for stock in stock_data:
	print(stock, "\n")
scraper.logout()

'''login_5 = session.get('https://www.nordnet.no/api/2/login')
try:
	session.headers.update({'ntag': login_5.headers['ntag']})
except KeyError:
	pass
print_req_info(login_5, "GET LOGIN CONFIRMATION")'''
