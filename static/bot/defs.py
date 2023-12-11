import sqlite3
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import *
import requests
from bs4 import BeautifulSoup as bs
import re


async def revalut(valut1, valut2, summ, id):

	url = f"https://www.xe.com/currencyconverter/convert/?Amount={summ}&From={valut1}&To={valut2}"
	content = requests.get(url).content
	soup = bs(content, "html.parser")
	exchange_rate_html = soup.find_all("p")[2]
	newsumm = exchange_rate_html.text
	newsumm = newsumm[:newsumm.find(".")+3]
	newsumm = newsumm.replace(",", "")
	
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("UPDATE users SET valut = ?, balance = ? WHERE id = ?",(valut2, newsumm, id,))
	con.commit()

	


def editmamont(id):
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("SELECT id, name, balance, status, valut, minpopoln, verif, boss, lasttrade, link, vivod, minvivod, blockvivod, blocktrade FROM users WHERE id = ?",(id,))
	user = cur.fetchone()
	if user[3] == 0:
		status = '🎲 Рандом'
	elif user[3] == 1:
		status = '👑 Выигрыш'
	elif user[3] == 2:
		status = '🏳️ Проигрыш'
	if user[5] == "0":
		user5 = 'Стандартное'
	else:
		user5 = user[5]

	if user[6] == 0:
		verif = "❌"

	elif user[6] == 1:
		verif = "✅"
	if user[7] != 0:
		try:
			boss = int(user[7])
			con = sqlite3.connect(workerbase)
			cur = con.cursor()
			cur.execute("SELECT id, name, link FROM workers WHERE id = ?",(boss,))
			worker = cur.fetchone()
			if worker[2] != None:
				wlink = f"<a href='https://t.me/{worker[2]}'>{worker[1]}</a>  🆔: <code>{worker[0]}</code>"
			else:
				wlink = f"<a href='tg://user?id={worker[0]}'>{worker[1]}</a>  🆔: <code>{worker[0]}</code>"
		except:
			wlink = "None"

	else:
		wlink = "None"

	if user[9] != None:
		user_link = f"<a href='https://t.me/{user[9]}'>{user[1]}</a>"
	else:
		user_link = f"<a href='tg://user?id={user[0]}'>{user[1]}</a>"

	if user[12] == 0:

		blockvivod = "🔓 доступен"

	elif user[12] == 1:

		blockvivod = "🔒 заблокирован"

	if user[13] == 0:

		blocktrade = "🔓 доступен"

	elif user[13] == 1:

		blocktrade = "🔒 заблокирован"

	try:
				
		minpopoln = int(user[5])
	except:

		limits = user[5].split(" ")

		if user[4] == "EUR":
			minpopoln = limits[0]
		elif user[4] == "USD":
			minpopoln = limits[1]
		elif user[4] == "UAH":
			minpopoln = limits[2]
		elif user[4] == "PLN":
			minpopoln = limits[3]
		elif user[4] == "RUB":
			minpopoln = limits[4]
		elif user[4] == "BYN":
			minpopoln = limits[5]

	try:
				
		minvivod = int(user[11])
	except:


		limits = user[11].split(" ")

		if user[4] == "EUR":
			minvivod = limits[0]
		elif user[4] == "USD":
			minvivod = limits[1]
		elif user[4] == "UAH":
			minvivod = limits[2]
		elif user[4] == "PLN":
			minvivod = limits[3]
		elif user[4] == "RUB":
			minvivod = limits[4]
		elif user[4] == "BYN":
			minvivod = limits[5]



	result = f"🦣 Информация о мамонте {user_link}\n🆔: <code>{user[0]}</code>\n👷🏿‍♂️ Воркер: {wlink}\n\n💰 Баланс мамонта\n├ Баланс: {user[2]} {user[4]}\n└ На выводе: {user[10]} {user[4]}\n\n🍀 Статус удачи: {status}\n\n🔐 Блокировки\n├ Трейд: {blocktrade}\n└ Вывод: {blockvivod}\n\n🔗 Минималки\n├ Мин.Пополнение: {minpopoln} {user[4]}\n└ Мин.Вывод: {minvivod} {user[4]}\n\n🪪 Статус верификации: {verif}\n\n📥 Результат последней ставки:\n{user[8]}\n\n♻️ Обновлено: "

	return result



