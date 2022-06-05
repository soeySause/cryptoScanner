from bs4 import BeautifulSoup
import requests
import yfinance
import pandas
import time


class CryptoScanner:

    @staticmethod
    def get_crypto_list():
        url = "https://finance.yahoo.com/cryptocurrencies/"
        page = requests.get(url, params={'count': '25', 'offset': '0'})

        soup = BeautifulSoup(page.content, "html.parser")

        crypto_list = soup.find(id="Lead-5-ScreenerResults-Proxy")
        list_elements = crypto_list.find_all("tr", class_="simpTblRow")

        tickers = ""

        for list_element in list_elements:
            tickers += list_element.find("a", class_="Fw(600)").text + " "

        return tickers.strip()

    @staticmethod
    def scan_cryptos(tickers):
        data = yfinance.download(tickers=tickers, period="5d", interval="5m")
        df = pandas.DataFrame(data)['Close']

        for col in df:
            df[col][0] = ((df[col].iloc[-2] - df[col].iloc[-14]) / df[col].iloc[-20] * 100)

            if df[col][0] > 1 or df[col][0] < -1:
                print(col + " has moved " + str(round(df[col][0], 2)) + "% in the last hour!")

        return 0


c_list = CryptoScanner.get_crypto_list()
while True:
    CryptoScanner.scan_cryptos(c_list)
    time.sleep(300)
