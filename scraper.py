# from alpha_vantage.timeseries import TimeSeries
# APIkey = 'PBO2NQEW58LZWI7U'
# ts = TimeSeries(key=APIkey, output_format='pandas')
# data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')


import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def get_listings_data(number_of_listings=100):
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
        listingInfo['CLOSE'] = float(priceClose[1])

        priceBuy = (listing.find_all('span', {'class': 'c02421'}))[3].decode_contents().replace("<!-- -->", '').split(
            " ")
        listingInfo['BUY'] = float(priceBuy[1])

        priceSell = (listing.find_all('span', {'class': 'c02421'}))[4].decode_contents().replace("<!-- -->", '').split(
            " ")
        listingInfo['SELL'] = float(priceSell[1])

        priceHigh = (listing.find('td', {'data-title': 'Høy'})).decode_contents().replace(',', '.')
        listingInfo['HIGH'] = float(priceHigh)

        priceLow = (listing.find('td', {'data-title': 'Lav'})).decode_contents().replace(',', '.')
        listingInfo['LOW'] = float(priceLow)

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


def array2csv_file():
    listingsData = get_listings_data()
    with open('current_data.csv', 'w', newline='', encoding="utf-8") as f:
        w = csv.DictWriter(f, listingsData[0].keys())
        w.writeheader()
        for listing in listingsData:
            w.writerow(listing)


def read_csv(*columns):
    columnNames = []
    if len(columns) == 0:
        columnNames = ["NAME", "HREF", "CHANGE_%", "CHANGE_NOK", "CLOSE", "BUY", "SELL", "HIGH", "LOW", "REVENUE_MNOK",
                       "TIME_HHMMSS", "TIME_SECS"]
    else:
        for column in columns:
            columnNames.append(column)

    df = pd.read_csv("current_data.csv")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 0):
        print(df[columnNames])


array2csv_file()
"""read_csv("NAME", "CHANGE_%", "CHANGE_NOK")"""
read_csv()
