# TODO: try login with import requests
#   session_requests = requests.session()
# login_url = "https://classic.nordnet.no/api/2/authentication/basic/login"
# result = session_requests.post(login_url, data=payload, headers=session.headers, cookies=session.cookies)

import SECRETS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

payload = {"username": SECRETS.NORDNET_username+"skdjfnskdnfj", "password": SECRETS.NORDNET_password}

url = "https://classic.nordnet.no/mux/login/startNO.html?clearEndpoint=0&intent=next"
