# from alpha_vantage.timeseries import TimeSeries
# APIkey = 'PBO2NQEW58LZWI7U'
# ts = TimeSeries(key=APIkey, output_format='pandas')
# data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')


import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import time
from time import sleep
from inspect import currentframe, getframeinfo
import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def get_listings_data_NORDNET(number_of_listings=100):
    URL = "https://www.nordnet.no/market/stocks?selectedTab=prices&sortField=diff_pct&sortOrder=desc&exchangeCountry=NO&exchangeList=no%3Aose"
    stockListingsPage = requests.get(URL).text

    soup = BeautifulSoup(stockListingsPage, 'lxml')
    stockTable = soup.find('tbody', class_='c02372')
    stockListings = stockTable.find_all('tr', class_="c02356 c02375")

    counter = 1
    listingsData = []
    for listing in stockListings:
        listingInfo = {}

        stockName = (listing.find('td', {'data-title': 'Navn'})).find('a', href=True)
        listingInfo['NAME'] = stockName.decode_contents()
        listingInfo['HREF'] = "https://www.nordnet.no/" + stockName['href']

        changePercent = (listing.find_all('span', {'class': 'c02421'}))[0].decode_contents().replace("<!-- -->",
                                                                                                     '').split(" ")
        listingInfo['CHANGE_%'] = float(changePercent[0] + changePercent[1])

        changeNOK = (listing.find_all('span', {'class': 'c02421'}))[1].decode_contents().replace("<!-- -->", '').split(
            " ")
        listingInfo['CHANGE_NOK'] = float(changeNOK[0] + changeNOK[1])

        priceClose = (listing.find_all('span', {'class': 'c02421'}))[2].decode_contents().replace("<!-- -->", '').split(
            " ")
        listingInfo['LAST'] = float(priceClose[1])

        priceBuy = (listing.find_all('span', {'class': 'c02421'}))[3].decode_contents().replace("<!-- -->", '').split(
            " ")
        listingInfo['BUY'] = float(priceBuy[1])

        priceSell = (listing.find_all('span', {'class': 'c02421'}))[4].decode_contents().replace("<!-- -->", '').split(
            " ")
        listingInfo['SELL'] = float(priceSell[1])

        priceHigh = (listing.find('td', {'data-title': 'Høy'})).decode_contents().replace(',', '.').replace(' ', '.')
        try:
            listingInfo['HIGH'] = float(priceHigh)
        except Exception:
            """listingInfo['HIGH'] = priceHigh"""
            continue

        priceLow = (listing.find('td', {'data-title': 'Lav'})).decode_contents().replace(',', '.').replace(' ', '.')
        try:
            listingInfo['LOW'] = float(priceLow)
        except Exception:
            """listingInfo['LOW'] = priceLow"""
            continue

        revenueMNOK = (listing.find_all('span', {'class': 'c02421'}))[5].decode_contents().replace("<!-- -->",
                                                                                                   '').split(" ")
        listingInfo['REVENUE_MNOK'] = (revenueMNOK[1])

        timeHHMMSS = (listing.find('td', {'data-title': 'Tid'})).find('span').decode_contents()
        listingInfo['TIME_HHMMSS'] = timeHHMMSS
        listingInfo['TIME_SECS'] = get_sec(timeHHMMSS)

        listingsData.append(listingInfo)

        if counter >= number_of_listings != 100:
            break
        counter += 1

    return listingsData


def get_listings_data_OSLOBORS(number_of_listings=250):  # USE int: -99 for unknown/invalid data
    URL = "https://www.oslobors.no/markedsaktivitet/#/list/shares/quotelist/ose/all/all/false"
    driver = webdriver.Chrome('C:\Windows/chromedriver.exe')
    driver.get(URL)

    sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[2]/ui-view/div/ui-view/div[4]/div/ui-view/div/quotes/table/thead/tr/th[8]/span').click()

    stockListingsPage = driver.page_source
    soup = BeautifulSoup(stockListingsPage, 'lxml')
    stockTable = soup.find('table', {'class': 'table table-striped stock-list-development'}).find('tbody')
    driver.close()

    stockListings = stockTable.find_all('tr', {'data-reactid': True})

    counter = 1
    listingsData = []
    for listing in stockListings:
        listingInfo = {}
        reactid = listing['data-reactid']

        listingInfo['SECTOR'] = listing.find('td', {'data-reactid': reactid + '.1'})['title']

        listingInfo['TICKER'] = listing.find('a', {'data-reactid': reactid + '.4.0'}).decode_contents()
        listingInfo['NAME'] = listing.find('a', {'data-reactid': reactid + '.5.0'}).decode_contents()
        listingInfo['HREF'] = 'https://www.oslobors.no/markedsaktivitet' + listing.find('a', {'data-reactid': reactid + '.5.0'})['href']

        listingInfo['LAST'] = float(listing.find('td', {'data-header': 'Siste'}).decode_contents().replace(',', '.').replace(' ', ''))

        changePercent = listing.find('td', {'data-header': 'Avk. % i dag'}).decode_contents().replace(',', '.').replace(' ', '')
        try:
            listingInfo['CHANGE_%'] = float(changePercent[:-1])
        except ValueError:
            listingInfo['CHANGE_%'] = -99

        priceSell = listing.find('td', {'data-header': 'Kjøper'}).decode_contents().replace(',', '.').replace(' ', '')
        priceBuy = listing.find('td', {'data-header': 'Selger'}).decode_contents().replace(',', '.').replace(' ', '')
        try:
            listingInfo['SELL'] = float()
            listingInfo['BUY'] = float()
        except ValueError:
            listingInfo['SELL'] = -99
            listingInfo['BUY'] = -99

        listingInfo['TURNOVER_MNOK'] = float(listing.find('td', {'data-header': 'Omsatt (MNOK)'}).decode_contents().replace(',', '.').replace(' ', ''))
        listingInfo['TRADES_COUNT'] = int(listing.find('td', {'data-header': 'Ant. handler'}).decode_contents())
        listingInfo['MARKETCAP_MNOK'] = float(listing.find('td', {'data-header': 'Markedsverdi (MNOK)'}).decode_contents().replace(',', '.').replace(' ', ''))

        t = time.localtime()
        timeHHMMSS = time.strftime("%H:%M:%S", t)
        listingInfo['TIME_HHMMSS'] = timeHHMMSS
        listingInfo['TIME_SECS'] = get_sec(timeHHMMSS)

        t = time.localtime()
        timeHHMMSS = time.strftime("%H:%M:%S", t)
        listingInfo['TIME_HHMMSS'] = timeHHMMSS
        listingInfo['TIME_SECS'] = get_sec(timeHHMMSS)

        listingsData.append(listingInfo)

        if counter >= number_of_listings:
            break
        counter += 1

    return listingsData


def array2csv_file(site):  # "NORDNET" for nordnet.no, "OSLOBØRS" for oslobors.no
    dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/current_data_log/'
    if site == "NORDNET":
        listingsData = get_listings_data_NORDNET()
        csvName = "NORDNET_" + str(int(time.time())) + ".csv"
    elif site == "DNB":
        listingsData = get_listings_data_DNB()
        csvName = "DNB_" + str(int(time.time())) + ".csv"
    elif site == "OSLOBORS":
        listingsData = get_listings_data_OSLOBORS()
        csvName = "OSLOBØRS_" + str(int(time.time())) + ".csv"
    path = os.path.join(dirPath, csvName)
    with open(path, 'w', newline='', encoding="utf-8") as f:
        w = csv.DictWriter(f, listingsData[0].keys())
        w.writeheader()
        for listing in listingsData:
            w.writerow(listing)
    return csvName


def read_csv(*file_rows_columns):  # Returns and prints read csv file. Specify file, columns with (FILENAME, NUMBEROFROWS, "ARG1", "ARG2", ...).
    dirPath = 'C:/Users/theba/PycharmProjects/StockTradingBot/current_data_log/'
    columnNames = []
    if len(file_rows_columns) == 1:
        columnNames = []
        rows = None
    elif len(file_rows_columns) == 2:
        columnNames = []
        rows = file_rows_columns[1]
    elif len(file_rows_columns) == 0:
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno, "ARGUMENT ERROR! Must specify atleast the file name.")
        return
    else:
        rows = file_rows_columns[1]
        counter = 0
        for column in file_rows_columns:
            if counter < 2:
                counter += 1
                continue
            columnNames.append(column)
            counter += 1

    path = os.path.join(dirPath, file_rows_columns[0])
    df = pd.read_csv(path, nrows=rows)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 0):
        if not columnNames:
            columnNames = df.columns
        print(df[columnNames])
        return df


def get_and_print_scraped_data_from_OBE(sorted_by='CHANGE_%', toPrint=1):
    listingsData = sorted(get_listings_data_OSLOBORS(), key=lambda i: i[sorted_by])
    if toPrint:
        print(listingsData)
    return listingsData


def get_and_print_scraped_data_from_NORDNET(sorted_by='CHANGE_%', toPrint=1):
    listingsData = sorted(get_listings_data_NORDNET(), key=lambda i: i[sorted_by])
    if toPrint:
        print(listingsData)
    return listingsData


"""NORDNET = get_and_print_scraped_data_from_NORDNET()
OBE = get_and_print_scraped_data_from_OBE()"""

"""print(next((item for item in NORDNET if item["NAME"] == OBE[-1]["NAME"]), None))"""

"""csvFile = array2csv_file("NORDNET")
read_csv(csvFile)"""