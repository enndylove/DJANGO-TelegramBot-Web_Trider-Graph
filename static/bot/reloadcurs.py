import requests
import sqlite3
from config import database, coinbase

def reloadcurs():

	r = requests.get('https://www.google.com/finance/quote/BTC-USD')
	marker = 'data-last-price='
	if marker in r.text:
		btc = float(r.text[r.text.find(marker)+17:r.text.find(marker)+24])
		#curs = curs[:curs.find("\xa0")]+curs[curs.find("\xa0")+1:]
		#curs = float(curs[:curs.find(",")]+"."+curs[curs.find(",")+1:])

	r = requests.get('https://www.google.com/finance/quote/ETH-USD')
	marker = 'data-last-price='

	if marker in r.text:
		eth = float(r.text[r.text.find(marker)+17:r.text.find(marker)+21])

	r = requests.get('https://www.google.com/finance/quote/BNB-USDT')
	marker = 'data-last-price='

	if marker in r.text:
		bnb = float(r.text[r.text.find(marker)+17:r.text.find(marker)+20])

	r = requests.get('https://www.google.com/finance/quote/DOGE-USD')
	marker = 'data-last-price='

	if marker in r.text:
		doge = float(r.text[r.text.find(marker)+17:r.text.find(marker)+23])

	r = requests.get('https://www.google.com/finance/quote/AMZN:NASDAQ')
	marker = "data-last-price="
	if marker in r.text:
		amzn = float(r.text[r.text.find(marker)+17:r.text.find(marker)+22])

	r = requests.get('https://www.google.com/finance/quote/AAPL:NASDAQ')
	marker = "data-last-price="

	if marker in r.text:
		aapl = float(r.text[r.text.find(marker)+17:r.text.find(marker)+22])

	r = requests.get('https://www.google.com/finance/quote/TSLA:NASDAQ')
	marker = "data-last-price="

	if marker in r.text:
		tsla = float(r.text[r.text.find(marker)+17:r.text.find(marker)+22])

	r = requests.get('https://www.google.com/finance/quote/GOOGL:NASDAQ')
	marker = 'data-last-price='

	if marker in r.text:
		googl = float(r.text[r.text.find(marker)+17:r.text.find(marker)+22])

	r = requests.get('https://www.google.com/finance/quote/MSFT:NASDAQ')
	marker = "data-last-price="

	if marker in r.text:
		msft = float(r.text[r.text.find(marker)+17:r.text.find(marker)+22])







	con = sqlite3.connect(coinbase)
	cur = con.cursor()
	cur.execute("UPDATE coins SET Bitcoin = ?, Ethereum = ?, Binance = ?, DogeCoin = ?, Amazon = ?, Apple = ?, Tesla = ?, Google = ?, Microsoft = ?",(btc, eth, bnb, doge, amzn, aapl, tsla, googl, msft,))
	con.commit()

