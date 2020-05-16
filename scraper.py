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


def get_listings_data_DNB(number_of_listings=250):  # WIP
    URL = "https://www.dnb.no/segm/appo/bov/open"
    driver = webdriver.Chrome('C:\Windows/chromedriver.exe')
    driver.get(URL)

    sleep(1)
    driver.find_element_by_xpath('//*[@id="consent-accept"]/span/a').click()

    showMoreRowsBtn = driver.find_element_by_xpath('//*[@id="nemoMarketList_showMoreRows"]/a')
    showMoreRowsBtn.click()
    sleep(1)

    stockListingsPage = driver.page_source
    soup = BeautifulSoup(stockListingsPage, 'lxml')
    stockTable = soup.find('table', {'id': 'nemoMarketList', 'class': 'ui-jqgrid-btable'})
    driver.close()

    stockListings = []
    stockListings = stockTable.find_all('tr', {'class': 'ui-widget-content jqgrow ui-row-ltr'})

    """columnNames = ["NAME", "HREF", "CHANGE_%", "CHANGE_NOK", "CLOSE", "BUY", "SELL", "HIGH", "LOW", "REVENUE_MNOK",
                      "TIME_HHMMSS", "TIME_SECS"]"""

    counter = 1
    listingsData = []
    for listing in stockListings:
        listingInfo = {}

        stockTicker = (listing.find('td', {'aria-describedby': 'nemoMarketList_wTicker'})).decode_contents()
        listingInfo['TICKER'] = stockTicker

        stockName = (listing.find('td', {'aria-describedby': 'nemoMarketList_wDescription'})).decode_contents()
        listingInfo['NAME'] = stockName

        lastCheckedPrice = (listing.find('td', {'aria-describedby': 'nemoMarketList_wLastDisplayPrice'})).decode_contents().replace(',', '.').replace(' ', '')
        listingInfo['LAST'] = float(lastCheckedPrice)

        changeNOK = (listing.find('td', {'aria-describedby': 'nemoMarketList_wNetChange'})).decode_contents().replace(',', '.').replace(' ', '')
        listingInfo['CHANGE_NOK'] = float(changeNOK)

        changePercent = (listing.find('td', {'aria-describedby': 'nemoMarketList_wPctChange'})).decode_contents().replace(',', '.').replace(' ', '')
        listingInfo['CHANGE_%'] = float(changePercent)

        priceSell = (listing.find('td', {'aria-describedby': 'nemoMarketList_wBidPrice'})).decode_contents().replace(',', '.').replace(' ', '')
        listingInfo['SELL'] = float(priceSell)

        priceBuy = (listing.find('td', {'aria-describedby': 'nemoMarketList_wAskPrice'})).decode_contents().replace(',', '.').replace(' ', '')
        listingInfo['BUY'] = float(priceBuy)

        priceHigh = (listing.find('td', {'aria-describedby': 'nemoMarketList_wHighPrice'})).decode_contents().replace(',', '.').replace(' ', '')
        try:
            listingInfo['HIGH'] = float(priceHigh)
        except ValueError:
            listingInfo['HIGH'] = float(-1)

        priceLow = (listing.find('td', {'aria-describedby': 'nemoMarketList_wLowPrice'})).decode_contents().replace(',', '.').replace(' ', '')
        try:
            listingInfo['LOW'] = float(priceLow)
        except ValueError:
            listingInfo['LOW'] = float(-1)

        totalValue = (listing.find('td', {'aria-describedby': 'nemoMarketList_wTotalValue'})).decode_contents().replace(',', '.').replace(' ', '')
        if totalValue != '0':
            totalValue = totalValue[:-1]
        listingInfo['VALUE_MNOK'] = float(totalValue)

        priceClose = (listing.find('td', {'aria-describedby': 'nemoMarketList_wLastDisplayClosePrice'})).decode_contents().replace(',', '.').replace(' ', '')
        listingInfo['CLOSE'] = float(priceClose)

        t = time.localtime()
        timeHHMMSS = time.strftime("%H:%M:%S", t)
        listingInfo['TIME_HHMMSS'] = timeHHMMSS
        listingInfo['TIME_SECS'] = get_sec(timeHHMMSS)

        listingsData.append(listingInfo)

        if counter >= number_of_listings != 100:
            break
        counter += 1

    return listingsData


def get_listings_data_OSLOBORS(number_of_listings=250):  # WIP
    URL = "https://www.oslobors.no/markedsaktivitet/#/list/shares/quotelist/ose/all/all/false"
    driver = webdriver.Chrome('C:\Windows/chromedriver.exe')
    driver.get(URL)

    sleep(1)
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
            listingInfo['CHANGE_%'] = changePercent

        priceSell = listing.find('td', {'data-header': 'Kjøper'}).decode_contents().replace(',', '.').replace(' ', '')
        priceBuy = listing.find('td', {'data-header': 'Selger'}).decode_contents().replace(',', '.').replace(' ', '')
        try:
            listingInfo['SELL'] = float()
            listingInfo['BUY'] = float()
        except ValueError:
            listingInfo['SELL'] = priceSell
            listingInfo['BUY'] = priceBuy

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
    if site == "NORDNET":
        listingsData = get_listings_data_NORDNET()
        csvName = "NORDNET_" + str(int(time.time())) + ".csv"
    elif site == "DNB":
        listingsData = get_listings_data_DNB()
        csvName = "DNB_" + str(int(time.time())) + ".csv"
    elif site == "OSLOBORS":
        listingsData = get_listings_data_OSLOBORS()
        csvName = "OSLOBØRS_" + str(int(time.time())) + ".csv"
    with open(csvName, 'w', newline='', encoding="utf-8") as f:
        w = csv.DictWriter(f, listingsData[0].keys())
        w.writeheader()
        for listing in listingsData:
            w.writerow(listing)
    return csvName


def read_csv(*file_rows_columns):  # Returns and prints read csv file. Specify file, columns with (FILENAME, NUMBEROFROWS, "ARG1", "ARG2", ...).
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

    df = pd.read_csv(file_rows_columns[0], nrows=rows)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 0):
        if not columnNames:
            columnNames = df.columns
        print(df[columnNames])
        return df


csvFile = array2csv_file("OSLOBORS")
read_csv(csvFile)
