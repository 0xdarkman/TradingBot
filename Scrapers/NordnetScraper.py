import requests
import SECRETS

session = requests.session()


def print_req_info(REQUEST_VARIABLE, REQUEST_DESCRIPTION, PRINT_CONTENT=True):
	if PRINT_CONTENT:
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


session.headers.update({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})
login_page = session.get('https://classic.nordnet.no/mux/login/startNO.html?clearEndpoint=0&intent=next')
print_req_info(login_page, "GET LOGIN PAGE", PRINT_CONTENT=False)


login_1 = session.post('https://classic.nordnet.no/api/2/login/anonymous')
session.headers.update({'ntag': login_1.headers['ntag']})
print_req_info(login_1, "POST LOGIN ANONYMOUS")


payload = {'username': SECRETS.NORDNET_username, 'password': SECRETS.NORDNET_password}
login_2 = session.post('https://classic.nordnet.no/api/2/authentication/basic/login', data=payload)
session.headers.update({'ntag': login_2.headers['ntag']})
print_req_info(login_2, "POST LOGIN LOGIN")


login_3 = session.get('https://classic.nordnet.no/api/2/customers/required_actions')
session.headers.update({'ntag': login_3.headers['ntag']})
print_req_info(login_3, "GET LOGIN REQUIRED")


login_4 = session.get('https://classic.nordnet.no/oauth2/authorize?client_id=NEXT&response_type=code&redirect_uri=https://www.nordnet.no/oauth2/')
print_req_info(login_4, "GET LOGIN AUTHORIZE", PRINT_CONTENT=False)

'''login_5 = session.get('https://www.nordnet.no/api/2/login')
try:
	session.headers.update({'ntag': login_5.headers['ntag']})
except KeyError:
	pass
print_req_info(login_5, "GET LOGIN CONFIRMATION")'''

session.headers.update({'client-id': "NEXT", 'DNT': "1", 'Host': "www.nordnet.no", 'Referer': "https://www.nordnet.no/",
                        'Sec-Fetch-Dest': "empty", 'Sec-Fetch-Mode': "cors", 'Sec-Fetch-Site': "same-origin",
                        'x-nn-href': "https://www.nordnet.no/market/stocks?selectedTab=prices&sortField=turnover&sortOrder=desc&page=1&exchangeCountry=NO&exchangeList=no%3Aose"})
stock_list_page_1 = "https://www.nordnet.no/api/2/instrument_search/query/stocklist?sort_attribute=turnover_normalized&sort_order=desc&limit=100&offset=0&free_text_search=&apply_filters=exchange_country%3DNO%7Cexchange_list%3Dno%3Aose"
stock_list_page_2 = "https://www.nordnet.no/api/2/instrument_search/query/stocklist?sort_attribute=turnover_normalized&sort_order=desc&limit=100&offset=100&free_text_search=&apply_filters=exchange_country%3DNO%7Cexchange_list%3Dno%3Aose"
stock_list_page_3 = "https://www.nordnet.no/api/2/instrument_search/query/stocklist?sort_attribute=turnover_normalized&sort_order=desc&limit=100&offset=200&free_text_search=&apply_filters=exchange_country%3DNO%7Cexchange_list%3Dno%3Aose"
get_stock_list = session.get(stock_list_page_1)
print_req_info(get_stock_list, "GET STOCK LIST")