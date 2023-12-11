#!/usr/bin/python
# coding: utf-8

import sqlite3
import random
import requests
import traceback


from bs4 import BeautifulSoup as bs

import time
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



#TOKEN = "5747079650:AAH_tHsCXuYHMX_TOZEtoZRAxwZ9v7223wM"
TOKEN = "5417783032:AAF1-NoKPPi6IV4yJnMvVu0XGNFiZdWVAp0"

database = "workerbase.db"

admins = "5200240570 5730438502 5000455903 658257014"
#658257014
my = 5730438502
adam = "@melovemeeeeeee"
#-882134200
#workchat = -1001841620603
#logs_id = -1001697550223
#canal_id = -1001864037994
#zay_id = -832530327
workchat = -882134200
canal_id = -882134200
logs_id = -882134200
zay_id = -882134200

admintext = "<b>Админка:\n\nДоступные команды:\n\n/profit - добавить профит.\n/addworker - добавить воркера.\n/delworker - удалить воркера.\n/reloadworkers - обновить базу воркеров.\n/spam - рассылка.</b>\n\n<i>Для доп. информации нажми на команду!</i>"


async def kursconvert(valut1, valut2, summ):

	url = f"https://www.xe.com/currencyconverter/convert/?Amount={summ}&From={valut1}&To={valut2}"
	content = requests.get(url).content
	soup = bs(content, "html.parser")
	exchange_rate_html = soup.find_all("p")[2]
	newsumm = exchange_rate_html.text
	newsumm = newsumm[:newsumm.find(".")+3]
	newsumm = newsumm.replace(",", "")
	
	return newsumm


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

class zayavka(StatesGroup):

	first = State()
	second = State()
	third = State()

class worker(StatesGroup):

	profit = State()
	status = State()
	pagehandler = State()
	idhandler = State()

def mainkb(id):

	if str(id) in admins:
		markup = ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)
		btn1 = KeyboardButton("Админ")

		markup.row(btn1)

		return markup

def soglkey():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "✅ Принять ✅", callback_data = "sogl")
	markup.row(btn1)

	return markup

def closekb():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "❌ Закрыть", callback_data = "close")
	markup.row(btn1)

	return markup

def zayotmena():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "🔙 Отмена", callback_data = "zayotmena")
	markup.row(btn1)

	return markup

def zaycomplete(id):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "↗️ Отправить", callback_data=  f"zaycomplete {id}")
	btn2 = InlineKeyboardButton(text = "🔄 Заново", callback_data = "rezay")
	btn3 = InlineKeyboardButton(text = "🔙 Отмена", callback_data = "zayotmena")
	markup.row(btn1,btn2).row(btn3)

	return markup

def zaykb():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "📝 Подать заявку", callback_data = "zapolnzay")
	markup.row(btn1)

	return markup

def adminsres(id):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "✔️", callback_data=  f"prin {id}")
	btn2 = InlineKeyboardButton(text = "✖️", callback_data = f"neprin {id}")
	markup.row(btn1,btn2)

	return markup


def menukb():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "👤 Профиль", callback_data = "profile")
	btn2 = InlineKeyboardButton(text = "🤖 Боты", callback_data = "bots")
	btn3 = InlineKeyboardButton(text = "ℹ️ Информация", callback_data = "info")

	markup.row(btn1).row(btn2).row(btn3)

	return markup

def profilekb():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "🔝 Топы 🔝", callback_data = "top")
	btn2 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn1).row(btn2)

	return markup

def adminkb():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "👷🏿‍♂️ Воркеры", callback_data = "workers")
	btn2 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn1).row(btn2)

	return markup

def startkb():
	markup = ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)
	btn1 = KeyboardButton("/start")

	markup.row(btn1)

	return markup

def profitkb():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "✔️", callback_data = "close")
	btn2 = InlineKeyboardButton(text = "✖️", callback_data = "close")

	markup.row(btn1, btn2)

	return markup

async def topfunc(message, reply):
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("SELECT id, name, profits, bank, link FROM workers")
	info = cur.fetchall()

	top = []
	topsumm = [0]
	test = True
	
	for info in info:
		i = 0
		while test == True:
			if float(info[3]) > float(topsumm[i]):
				if info[4] != "" and info[4] != None:
					userlink = f"<a href='http://t.me/{info[4]}'>{info[1]}</a>"
				else:
					userlink = f"<a href='tg://user?id={info[0]}'>{info[1]}</a>"
				topsumm.insert(i, info[3])
				if int(info[2]) >=5 and int(info[2]) <= 20:
					profit = "профитов"
				else:
					num = int(info[2][-1])
					if num == 1:
						profit = "профит"
					elif num >=2 and num <= 4:
						profit = "профита"
					elif num >=5 and num <= 9 or num == 0:
						profit = "профитов"

				if "." in info[3]:
					summ = info[3][:info[3].find('.')]
				else:
					summ = info[3]
				top.insert(i, f"{userlink} ~ {summ} USD - {info[2]} {profit}")
				test = False
			else:
				if i + 1 < len(topsumm):
					i = i + 1
				else:
					test = False
					
		test = True
	alltop = 0
	for topsumm in topsumm:
		alltop = alltop + float(topsumm)
	alltop = str(alltop)[:str(alltop).find('.')]
	allgrn = await kursconvert('USD', 'UAH', alltop)
	allgrn = str(allgrn)[:str(allgrn).find('.')]			
	text = ""
	i = 0
	n = 1
	while i < 10:
		try:
			text = f"{text}\n{n}. {top[i]}"
			i = i + 1
			n = n + 1
		except:
			break

	await bot.send_message(message.chat.id, f"<b>👊 Топ 10 воркеров\n\n🌟 Общая касса: {alltop} USD ~ {allgrn} UAH\n{text}</b>", parse_mode = "HTML", reply_to_message_id = reply, disable_web_page_preview = True)


def workers(page):
	try:
		con = sqlite3.connect(database)
		cur = con.cursor()
		cur.execute("SELECT id, name, profits FROM workers")
		info = cur.fetchall()

		topprofit = [0]
		newlist = []
		test = True

		for info in info:
			i = 0
			while test == True:
				if int(info[2]) >= int(topprofit[i]):
					topprofit.insert(i, info[2])
					tup = ((info[0]), (info[1]))
					newlist.insert(i, tup)
					test = False
				else:
					if i + 1 <= len(newlist):
						i = i + 1
					else:
						test = False
			test = True

		id = newlist


		if page == 1:
			minmam = 0
			maxmam = 9
		else:
			minmam = (page - 1) * 10
			maxmam = minmam + 9

		markup = InlineKeyboardMarkup()
		i = 0
		pagei = 0
		for id in id:
			try:
				if i >= minmam and i <= maxmam:
					if id[1] == None:
						name = "неизвестен"
					else:
						name = id[1]
					btn = InlineKeyboardButton(text = f"{name}", callback_data = f"worker {id[0]}")
					markup.row(btn)
				i = i + 1

			except:
				pagei = 0
		while i > 0:
			i = i - 10
			pagei = pagei + 1

		if pagei == 0 or pagei == 1:
			pagecalldata = "none"
		else:
			pagecalldata = f"pagehandler {pagei}"

		btn1 = InlineKeyboardButton(text='⬅️', callback_data = f"< {page} {pagei}")
		btn2 = InlineKeyboardButton(text=f'{page}/{pagei}',callback_data = pagecalldata)
		btn3 = InlineKeyboardButton(text='➡️', callback_data=f"> {page} {pagei}")
		btn4 = InlineKeyboardButton(text='♻️ Обновить ♻️',callback_data = "reloadworkerslist")
		btn5 = InlineKeyboardButton(text='Ввести ид', callback_data = "idhandler")
		btn6 = InlineKeyboardButton(text='❌ Закрыть ❌',callback_data = "close")
		markup.row(btn1, btn2, btn3).row(btn4).row(btn5).row(btn6)


		return markup
	except Exception as e:
		error = traceback.format_exc()
		line = error[error.find("line") + 5:]
		line = line[:line.find(", in ")]
		print(f"Ошибка:\n\n{e}\n\nСтрока: {line}")


def editworker(id):
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("SELECT id, name, link, regdate, status, profits, bank FROM workers WHERE  id = ?", (id, ))
	info = cur.fetchone()

	if info[2] != None:
		user_link = f"<a href='https://t.me/{info[2]}'>{info[1]}</a>"
	else:
		user_link = f"<a href='tg://user?id={info[0]}'>{info[1]}</a>"

	if info[4] != "0":
		status = info[4]
	else:

		if int(info[4]) == 0:
			status = "Мамонт 🦣"

		elif int(info[4]) < 10:
			status = "Новокек 🌱"

		elif int(info[4]) < 25:
			status = "Прошаренный 👨‍🏭"

		elif int(info[4]) < 50:
			status = "Задрот 👨‍💻"

		else:
			status = "Ёбырь 🦣"

	text = f"<b>👷🏿‍♂️ Воркер:{user_link} 🆔: <code>{info[0]}</code>\n\n📅 Дата регистрации: {info[3]}\n📌 Статус: {status}\n💰 Профитов: {info[5]} на сумму: {info[6]} USD</b>"

	return text

def workerkey(id):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "➕ Профит", callback_data = f"profit {id}")
	btn2 = InlineKeyboardButton(text = "📌 Статус", callback_data = f"status {id}")
	btn3 = InlineKeyboardButton(text = "🗑 Удалить", callback_data = f"deletewor {id}")
	btn4 = InlineKeyboardButton(text = "❌ Закрыть", callback_data = "close")

	markup.row(btn1).row(btn2).row(btn3).row(btn4)

	return markup

def yesdel(id):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "👌 Да", callback_data = f"yesdeletewor {id}")
	btn2 = InlineKeyboardButton(text = "🙅 Нет", callback_data = f"nodeletewor {id}")

	markup.row(btn1).row(btn2)

	return markup

@dp.callback_query_handler(state = "*")
async def answer(call, state: FSMContext):

	try:
		if call.data == "sogl":

			await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = "<b>⭐️ Приветствуем тебя, для того чтобы подать заявку ответь на пару вопросов.</b>\n\nОтвечай на вопросы корректно и твоя заявка обязательно будет принята.", parse_mode = "HTML", reply_markup = zaykb())

		elif call.data == "zapolnzay":

			msg = await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = "<b>Твоя заявка: Не заполнена!\n\n1. 🪐 Откуда ты узнал о нашей команде?</b>", parse_mode = "HTML", reply_markup = zayotmena())
			await zayavka.first.set()

			async with state.proxy() as data:
				data['msg'] = msg.message_id

		elif call.data == "zayotmena":

			await state.finish()
			await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = "<b>⭐️ Приветствуем тебя, для того чтобы подать заявку ответь на пару вопросов.</b>\n\nОтвечай на вопросы корректно и твоя заявка обязательно будет принята.", parse_mode = "HTML", reply_markup = zaykb())

		elif call.data[:11] == "zaycomplete":

			await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = f"<b>Твоя заявка: Отправлена!\n\n{call.message.text[25:]}\n\nЖди решения администрации</b>", parse_mode = "HTML")
			await bot.send_message(zay_id, f"<b>Новый желающий в тиму: @{call.message.chat.username}!\n\n{call.message.text[25:]}</b>", parse_mode = "HTML", reply_markup = adminsres(call.data[12:]))

		elif call.data[:4] == "prin":

			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute(f"INSERT INTO workers (id, regdate) VALUES ({call.data[5:]}, \"{str(call.message.date)[:10]}\")")
			con.commit()

			await bot.delete_message(call.message.chat.id, call.message.message_id)
			await bot.send_message(call.data[5:], "<b>Поздравляем,ваша заявка успешно принята ✅</b>", parse_mode = "HTML")
			await bot.send_message(call.data[5:], "<b>💨 Welcome\n\n<a href='https://t.me/+Y1vkv7HZCBMyMmRi'>🔮 Наш чат (тык)</a>\n\n<a href='https://t.me/+R4tFa5SkE7hjZmFi'>💰 Канал оплат (тык)</a>\n\n<a href='https://t.me/+Fl8ekox5HQtkN2Ey'>⚡️ Материалы для работы (тык)</a></b>\n\n🛑 Для более детальной информации напиши в чате /rules", parse_mode = "HTML", reply_markup = menukb())

		elif call.data[:6] == "neprin":

			await bot.delete_message(call.message.chat.id, call.message.message_id)
			await bot.send_message(call.data[7:], "<b>Вам отказано!")


		elif call.data == "profile":
			await call.answer("⏳ Момент")
			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute("SELECT profits, bank, clearbank, regdate, status FROM workers WHERE id = ?", (call.message.chat.id,))
			info = cur.fetchone()

			if info[4] != "0":
				status = info[4]
			else:

				if int(info[0]) == 0:
					status = "Мамонт 🦣"

				elif int(info[0]) < 10:
					status = "Новокек 🌱"

				elif int(info[0]) < 25:
					status = "Прошаренный 👨‍🏭"

				elif int(info[0]) < 50:
					status = "Задрот 👨‍💻"

				else:
					status = "Ёбырь 🦣"

			profilepic = await dp.bot.get_user_profile_photos(call.message.chat.id)

			uah = await kursconvert("USD", "UAH", info[1])
			rub = await kursconvert("USD", "RUB", info[1])
			clearuah = await kursconvert("USD", "UAH", info[2])
			clearrub = await kursconvert("USD", "RUB", info[2])

			await bot.send_photo(call.message.chat.id, profilepic.photos[0][0].file_id, f"<b>👤 Профиль\n\n{call.message.chat.full_name}\n🆔: <code>{call.message.chat.id}</code>\n🗽Статус: {status}\n⏳С нами от: {info[3]}\n\n💸 Количество профитов: {info[0]}\n\n🏦 Сумма профитов:\n{uah} UAH ~ {rub} RUB</b>", parse_mode = "HTML", reply_markup = profilekb())

		elif call.data == "top":
			await topfunc(call.message, 0)
			await call.answer()
			
		elif call.data == "close":
			await state.finish()
			await bot.delete_message(call.message.chat.id, call.message.message_id)


		elif call.data == "bots":
			await state.finish()
			await bot.send_message(call.message.chat.id, f"<b>🤖 Боты\n\n@BitZlatoMargin_bot\nТвоя реферальная ссылка: <code>http://t.me/BitZlatoMargin_bot?start={call.message.chat.id}</code></b>", disable_web_page_preview = True, parse_mode = "HTML", reply_markup = closekb())
			await call.answer()

		elif call.data == "info":
			await bot.send_message(call.message.chat.id, "<b>⭐️Hiwent Team\n=====================\n•👾Процент оплат :\n•75% - первое пополнение\n•60% - пополнение через   поддержку\n•75% - пополнение через прямой перевод\n\n•🥷(ТС/Кодер) - @ded_fresko\n\n•👹Вопросы по ворку - @melovemeeeeeee\n×××××××××××××××××××××××\n•Работаем : 🇺🇦🇷🇺🇵🇱🇪🇺🇧🇾🇺🇸\n×××××××××××××××××××××××</b>", parse_mode = "HTML", reply_markup = closekb())
			await call.answer()

		elif call.data == "rezay":

			msg = await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = "<b>Твоя заявка: Не заполнена!\n\n1. 🪐 Откуда ты узнал о нашей команде?</b>", parse_mode = "HTML", reply_markup = zayotmena())
			await zayavka.first.set()

			async with state.proxy() as data:
				data['msg'] = msg.message_id
	

		elif call.data == "workers":
			await call.answer()
			await bot.send_message(call.message.chat.id, "<b>📑 Список воркеров</b>", parse_mode = "HTML", reply_markup = workers(1))

		elif call.data == "reloadworkerslist":
			try:
				await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = "<b>📑 Список воркеров</b>", parse_mode = "HTML", reply_markup = workers(1))
				await call.answer("✅ Обновлено")
			except:
				await call.answer("⚠️ Изменений нет")

		elif call.data[:1] == ">":
			info = str(call.data).split(" ")
			if int(info[1]) + 1 > int(info[2]):
				page = 1
			else:
				page = int(info[1]) + 1

			await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = "<b>📑 Список воркеров</b>", parse_mode = "HTML", reply_markup = workers(page))

		elif call.data[:11] == "pagehandler":
			await call.answer(f"⚠️ Доступно страниц: {call.data[12:]}")
			msg = await bot.send_message(call.message.chat.id, "<b>📑 Введи номер странички</b>", parse_mode = "HTML", reply_markup = closekb())
			await worker.pagehandler.set()

			async with state.proxy() as data:
				data["pagehandler"] = call, msg.message_id

		elif call.data[:9] == "idhandler":
			await call.answer("⚠️ Введи ид воркера")
			msg = await bot.send_message(call.message.chat.id, "<b>📑 Введи ID</b>", parse_mode = "HTML", reply_markup = closekb())
			await worker.idhandler.set()

			async with state.proxy() as data:
				data["idhandler"] = msg.message_id

		elif call.data[:1] == "<":
			info = str(call.data).split(" ")
			if int(info[1]) - 1 == 0:
				page = int(info[2])
			else:
				page = int(info[1]) - 1

			await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = "<b>📑 Список воркеров</b>", parse_mode = "HTML", reply_markup = workers(page))

		elif call.data[:6] == "worker":
			await bot.send_message(call.message.chat.id, f"{editworker(call.data[7:])}", parse_mode = "HTML", disable_web_page_preview = True, reply_markup = workerkey(call.data[7:]))
			await call.answer()

		elif call.data[:9] == "deletewor":
			await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = "<b>⚠️ Удалить воркера?</b>", parse_mode = "HTML", reply_markup = yesdel(call.data[10:]))

		elif call.data[:12] == "yesdeletewor":
			id = call.data[13:]
			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute("DELETE FROM workers WHERE id = ?",(id,))
			con.commit()
			await call.answer("✅ Готово")
			await bot.delete_message(call.message.chat.id, call.message.message_id)

		elif call.data[:11] == "nodeletewor":
			await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,text = editworker(call.data[12:]), parse_mode = "HTML", disable_web_page_preview = True, reply_markup = workerkey(call.data[12:]))

		elif call.data[:6] == "status":
			await call.answer("⚠️ Cтатус будет отображаться в профиле")
			msg = await bot.send_message(call.message.chat.id, "<b>✍️ Введи новый статус для воркера</b>", parse_mode = "HTML", reply_markup = closekb())

			await worker.status.set()

			async with state.proxy() as data:
				data['msg'] = msg.message_id
				data["msg2"] = call.message.message_id
				data['id'] = call.data[7:]


		elif call.data[:6] == "profit":
			await call.answer("Сумма валюта процент страна\n\n⚠️ Разделяй пробелами", show_alert = True)
			msg = await bot.send_message(call.message.chat.id, "<b>✍️ Введи данные профита</b>", parse_mode = "HTML", reply_markup = closekb())

			await worker.profit.set()

			async with state.proxy() as data:
				data['msg'] = msg.message_id
				data["msg2"] = call.message.message_id
				data['id'] = call.data[7:]



	except Exception as e:
		error = traceback.format_exc()
		line = error[error.find("line") + 5:]
		line = line[:line.find(", in ")]
		print(f"Ошибка:\n\n{e}\n\nСтрока: {line}")

@dp.message_handler(lambda message: message.chat.type == "private", commands = ["start"], state = "*")
async def start(message: types.Message, state: FSMContext):

	await state.finish()

	inchat = await bot.get_chat_member(chat_id = workchat, user_id = message.chat.id)

	if inchat["status"] != 'left':
		await bot.send_message(message.chat.id, "<b>Приветствуем тебя снова 🤝</b>", parse_mode = "HTML", reply_markup = startkb())
		await bot.send_message(message.chat.id, "<b>💨 Welcome\n\n<a href='https://t.me/+Y1vkv7HZCBMyMmRi'>🔮 Наш чат (тык)</a>\n\n<a href='https://t.me/+R4tFa5SkE7hjZmFi'>💰 Канал оплат (тык)</a>\n\n<a href='https://t.me/+Fl8ekox5HQtkN2Ey'>⚡️ Материалы для работы (тык)</a></b>\n\n🛑 Для более детальной информации напиши в чате /rules", parse_mode = "HTML", reply_markup = menukb())
		if str(message.chat.id) in admins:
			await bot.send_message(message.chat.id, "Ку админ:)", reply_markup = mainkb(message.chat.id))
		con = sqlite3.connect(database)
		cur = con.cursor()
		cur.execute("UPDATE workers SET name = ?, link = ? WHERE id = ?", (message.chat.first_name, message.chat.username, message.chat.id,))
		con.commit()
	else:

		await bot.send_message(message.chat.id,"<b>⛔️ Правилами запрещено:\n✖️ Использовать свои кошельки для приёма платежей.\n✖️ Пытаться обмануть администрацию в разных аспектах\n✖️ Неадекватное поведение\n✖️ Реклама сторонних проектов/услуг\n✖️ Попрошайничество\n✖️ Распространение запрещённых материалов\n✖️ Дизинформация о проектах\n✖️ Отправка гифок, стикеров, фотографий, видео 18+</b>", parse_mode = "HTML", reply_markup = soglkey())


@dp.message_handler(lambda message: message.chat.type == "private" and str(message.chat.id) in str(admins), commands = ["profit"], state = None)
async def profit(message: types.Message, state: FSMContext):

	if message.text == "/profit" and str(message.chat.id) in admins:

		await bot.delete_message(message.chat.id, message.message_id)
		await bot.send_message(message.chat.id, "<b>Команда должна иметь такой вид:\n\n'/profit ID(ставь прочерк '-' если нет ID) Линк(@линк) Сумма Валюта Процент Страна(Украина 🇺🇦)'</b>\n\n<i>Если воркер отсутствует ставь '-'\nЗначения указывать через пробел!</i>", parse_mode = "HTML", reply_markup = closekb()) 

	elif str(message.chat.id) in admins:

		try:
			text = message.text.split(" ")
			id = text[1]
			link = text[2].replace("@", "")
			if id == "0":
				try:
					con = sqlite3.connect(database)
					cur = con.cursor()
					cur.execute("SELECT id FROM workers WHERE link = ?", (link,))
					id = cur.fetchone()[0]
				except:
					await bot.send_message(message.chat.id, "<b>⚠️ Ошибка</b>\n\n<i>(попробуй ввести ID)</i>", parse_mode = "HTML")
	
			else:
				summ = text[3].replace(".", "")
				valut = text[4]
				percent = text[5]
				country = text[6]
				con = sqlite3.connect(database)
				cur = con.cursor()
				cur.execute("SELECT profits, bank, clearbank FROM workers WHERE id = ?", (id,))
				info = cur.fetchone()
				profits = int(info[0]) + 1
				if str(valut) == "USD":
					bank = float(info[1]) + float(summ)
					clearbank = float(info[2]) + (float(summ)/100*int(percent))
				else:
					newsumm = await kursconvert(valut, "USD", summ)
					bank = float(info[1]) + float(newsumm)
					clearbank = float(info[2]) + (float(newsumm)/100*int(percent))

				con = sqlite3.connect(database)
				cur = con.cursor()
				cur.execute("UPDATE workers SET profits = ?, bank = ?, clearbank = ? WHERE id = ?",(profits, bank, clearbank, id,))
				con.commit()
				
				await bot.send_message(id, f"<b>👊 Успешное пополнение\n💸 Сумма: (~{summ}~{valut}) 🟢\n💸 Сумма чистых: (~{float(summ)/100*int(percent)}~{valut}) 🟢\n🥷Статус выплаты: ❌\nВыплата ~({percent}%)~\n\nЗа выплатой к {adam}</b>", parse_mode = "HTML")
				await bot.send_message(my, f"<b>👊 Успешное пополнение\n💸 Сумма: (~{summ}~{valut})\n💸 Мой проц: {float(summ)/10} {valut}</b>", parse_mode = "HTML")	
				await bot.send_message(canal_id, f"<b>👊 Успешное пополнение\n🌍 {country}\n💸 Сумма: (~{summ} {valut}~)\n👩‍🚀 Воркер: @{link}\n💰 Процент (~{percent}%~)\n🌟 Статус выплаты: ❌</b>", parse_mode = "HTML")
				await bot.send_message(message.chat.id, "<b>✔️ Готово</b>", parse_mode = "HTML")

		except Exception as e:
			error = traceback.format_exc()
			line = error[error.find("line") + 5:]
			line = line[:line.find(", in ")]
			print(f"Ошибка:\n\n{e}\n\nСтрока: {line}")
			await bot.send_message(message.chat.id, "<b>⚠️ Ошибка</b>\n\n<i>Возможно указаны не все данные или неправильный формат(попробуй ввести ID)</i>", parse_mode = "HTML")

@dp.message_handler(lambda message: message.chat.type == "private" and str(message.chat.id) in str(admins), commands = ["addworker"], state = None)
async def addworker(message: types.Message, state: FSMContext):

	if message.text == "/addworker" and str(message.chat.id) in admins:

		await bot.delete_message(message.chat.id, message.message_id)
		await bot.send_message(message.chat.id, "<b>Команда должна иметь такой вид:\n\n'/addworker ID(воркера)'</b>\n\n<i>Значения указывать через пробел!</i>", parse_mode = "HTML", reply_markup = closekb()) 

	elif str(message.chat.id) in admins:

		id = message.text[11:]
		con = sqlite3.connect(database)
		cur = con.cursor()
		cur.execute("INSERT INTO workers (id, regdate) VALUES(?, ?)",(message.text[11:], str(message.date)[:10]))
		con.commit()

		await bot.send_message(message.chat.id, "<b>✔️ Готово</b>", parse_mode = "HTML")



@dp.message_handler(lambda message: message.chat.type == "private" and str(message.chat.id) in str(admins), commands = ["delworker"], state = None)
async def delworker(message: types.Message, state: FSMContext):

	if message.text == "/delworker" and str(message.chat.id) in admins:

		await bot.delete_message(message.chat.id, message.message_id)
		await bot.send_message(message.chat.id, "<b>Команда должна иметь такой вид:\n\n'/delworker ID(воркера)'</b>\n\n<i>Значения указывать через пробел!</i>", parse_mode = "HTML", reply_markup = closekb()) 


	elif str(message.chat.id) in admins:

		id = message.text[11:]
		con = sqlite3.connect(database)
		cur = con.cursor()
		cur.execute("DELETE FROM workers WHERE id = ?",(id,))
		con.commit()

		await bot.send_message(message.chat.id, "<b>✔️ Готово</b>", parse_mode = "HTML")


@dp.message_handler(lambda message: message.chat.type == "private" and str(message.chat.id) in str(admins), commands = ["reloadworkers"], state = None)
async def reloadworkers(message: types.Message, state: FSMContext):

	if str(message.chat.id) in admins:
		await bot.send_message(message.chat.id, "<b>Это займет некоторое время</b>", parse_mode = "HTML")
		try:

			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute("SELECT id FROM workers")
			info = cur.fetchall()

			dellist = []

			for info in info:
				try:
					inchat = await bot.get_chat_member(chat_id = workchat, user_id = info[0])
					inchat = inchat["status"]
					if inchat != None and inchat != "left":
						pass
					else:
						dellist.append((info[0],))
				except:
					dellist.append((info[0],))

			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.executemany("DELETE FROM workers WHERE id = ?",(dellist))
			con.commit()

			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute("SELECT id, name, link, regdate, profits, bank, clearbank FROM workers")
			info = cur.fetchall()

			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute("DELETE FROM workers")
			con.commit()

			newlist = []

			for info in info:

				if str(info[0]) in str(newlist):
					pass
				else:
					newlist.append(info)
			i = 0
			for newlist in newlist:
				con = sqlite3.connect(database)
				cur = con.cursor()
				cur.executemany("INSERT INTO workers(id, name, link, regdate, profits, bank, clearbank) VALUES (?,?,?,?,?,?,?)", (newlist,))
				con.commit()
				i = i + 1
			await bot.send_message(message.chat.id, "<b>✔️ Готово</b>", parse_mode = "HTML")
		except Exception as e:
			print(e)
			await bot.send_message(message.chat.id, "<b>⚠️ Ошибка</b>", parse_mode = "HTML")


@dp.message_handler(lambda message: message.chat.type == "private" and str(message.chat.id) in str(admins), commands = ["spam"], state = None)
async def spam(message: types.Message, state: FSMContext):

	if message.text == "/spam" and str(message.chat.id) in admins:
		await bot.delete_message(message.chat.id, message.message_id)
		await bot.send_message(message.chat.id, "<b>Команда должна иметь такой вид:\n\n'/spam Текст'</b>\n\n<i>Значения указывать через пробел!</i>", parse_mode = "HTML", reply_markup = closekb()) 

	elif str(message.chat.id) in admins:
		spamtext = message.text[5:]
		con = sqlite3.connect(database)
		cur = con.cursor()
		cur.execute("SELECT id FROM workers")
		id = cur.fetchall()

		for id in id:
			try:
				await bot.send_message(id[0], f"<b>{spamtext}</b>", parse_mode = "HTML")
			except:
				pass
		await bot.send_message(message.chat.id, "<b>✔️ Готово</b>", parse_mode = "HTML")




@dp.message_handler(lambda message: message.text[:4] == "/top", state = None)
async def topfunchd(message: types.Message, state: FSMContext):

	await topfunc(message, message.message_id)

@dp.message_handler(lambda message: message.text[:3] == "/me", state = None)
async def topfunchd(message: types.Message, state: FSMContext):

	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("SELECT profits, bank, clearbank, regdate, status FROM workers WHERE id = ?", (message.from_user.id,))
	info = cur.fetchone()

	if info[4] != "0":
		status = info[4]
	else:

		if int(info[0]) == 0:
			status = "Мамонт 🦣"

		elif int(info[0]) < 10:
			status = "Новокек 🌱"

		elif int(info[0]) < 25:
			status = "Прошаренный 👨‍🏭"

		elif int(info[0]) < 50:
			status = "Задрот 👨‍💻"

		else:
			status = "Ёбырь 🦣"

	uah = await kursconvert("USD", "UAH", info[1])
	rub = await kursconvert("USD", "RUB", info[1])
	clearuah = await kursconvert("USD", "UAH", info[2])
	clearrub = await kursconvert("USD", "RUB", info[2])

	await bot.send_message(message.chat.id, f"<b>👤 Профиль\n\n{message.from_user.full_name}\n🆔: <code>{message.from_user.id}</code>\n🗽Статус: {status}\n⏳С нами от: {info[3]}\n\n💸 Количество профитов: {info[0]}\n\n🏦 Сумма профитов:\n{uah} UAH ~ {rub} RUB</b>", parse_mode = "HTML", reply_to_message_id = message.message_id)



@dp.message_handler(lambda message: message.chat.type == "private" and str(message.chat.id) in str(admins), state = None)
async def menu(message: types.Message, state: FSMContext):

	if message.text == "Админ" and str(message.chat.id) in admins:
		await bot.delete_message(message.chat.id, message.message_id)
		await bot.send_message(message.chat.id, admintext, parse_mode = "HTML", reply_markup = adminkb()) 




@dp.message_handler(state = worker.status)
async def status(message: types.Message, state: FSMContext):

	text = message.text
	await bot.delete_message(message.chat.id, message.message_id)
	async with state.proxy() as data:
		id = data["id"]
		msg = data["msg"]
		msg2 = data["msg2"]
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("UPDATE workers SET status = ? WHERE id = ?",(text, id,))
	con.commit()

	await bot.delete_message(message.chat.id, msg)
	await bot.edit_message_text(chat_id = message.chat.id, message_id = msg2,text = editworker(id), parse_mode = "HTML", disable_web_page_preview = True, reply_markup = workerkey(id))



@dp.message_handler(state = worker.profit)
async def inlineprofit(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		id = data["id"]
		msg = data["msg"]
		msg2 = data["msg2"]

		try:
			text = message.text.split(" ")
			await bot.delete_message(message.chat.id, message.message_id)

			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute("SELECT link FROM workers WHERE id = ?", (id,))
			link = cur.fetchone()[0]

			summ = text[0].replace(".", "")
			valut = text[1]
			percent = text[2]
			country = text[3]
			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute("SELECT profits, bank, clearbank FROM workers WHERE id = ?", (id,))
			info = cur.fetchone()
			profits = int(info[0]) + 1
			if str(valut) == "USD":
				bank = float(info[1]) + float(summ)
				clearbank = float(info[2]) + (float(summ)/100*int(percent))
			else:
				newsumm = await kursconvert(valut, "USD", summ)
				bank = float(info[1]) + float(newsumm)
				clearbank = float(info[2]) + (float(newsumm)/100*int(percent))

			con = sqlite3.connect(database)
			cur = con.cursor()
			cur.execute("UPDATE workers SET profits = ?, bank = ?, clearbank = ? WHERE id = ?",(profits, bank, clearbank, id,))
			con.commit()
			
			await bot.send_message(id, f"<b>👊 Успешное пополнение\n💸 Сумма: (~{summ}~{valut}) 🟢\n💸 Сумма чистых: (~{float(summ)/100*int(percent)}~{valut}) 🟢\n🥷Статус выплаты: ❌\nВыплата ~({percent}%)~\n\nЗа выплатой к {adam}</b>", parse_mode = "HTML")
			await bot.send_message(my, f"<b>👊 Успешное пополнение\n💸 Сумма: (~{summ}~{valut})\n💸 Мой проц: {float(summ)/10} {valut}</b>", parse_mode = "HTML")	
			await bot.send_message(canal_id, f"<b>👊 Успешное пополнение\n🌍 {country}\n💸 Сумма: (~{summ} {valut}~)\n👩‍🚀 Воркер: @{link}\n💰 Процент (~{percent}%~)\n🌟 Статус выплаты: ❌</b>", parse_mode = "HTML")
			await bot.delete_message(message.chat.id, msg)
			await bot.edit_message_text(chat_id = message.chat.id, message_id = msg2,text = editworker(id), parse_mode = "HTML", disable_web_page_preview = True, reply_markup = workerkey(id))

			msg = await bot.send_message(message.chat.id, "<b>✔️ Готово</b>", parse_mode = "HTML")
			time.sleep(3)
			await bot.delete_message(message.chat.id, msg.message_id)

		except Exception as e:
			error = traceback.format_exc()
			line = error[error.find("line") + 5:]
			line = line[:line.find(", in ")]
			print(f"Ошибка:\n\n{e}\n\nСтрока: {line}")
			await bot.send_message(message.chat.id, "<b>⚠️ Ошибка</b>\n\n<i>Возможно указаны не все данные или неправильный формат(попробуй ввести ID)</i>", parse_mode = "HTML")



	await bot.delete_message(message.chat.id, msg)
	await bot.edit_message_text(chat_id = message.chat.id, message_id = msg2,text = editworker(id), parse_mode = "HTML", disable_web_page_preview = True, reply_markup = workerkey(id))


@dp.message_handler(state = worker.pagehandler)
async def pagehandlerhd(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		pagei = data["pagehandler"][0].data[12:]
		try:
			if int(message.text) <= int(pagei):
				await bot.edit_message_text(chat_id = message.chat.id, message_id = data["pagehandler"][1],text = "<b>📑 Список воркеров</b>", parse_mode = "HTML", reply_markup = workers(int(message.text)))
				await bot.delete_message(message.chat.id, message.message_id)
				await bot.delete_message(message.chat.id, data["pagehandler"][0].message.message_id)
			else:
				msg = await bot.send_message(message.chat.id, "⚠️ Такой страницы нет")
				await bot.delete_message(message.chat.id, message.message_id)
				time.sleep(3)
				await bot.delete_message(message.chat.id, msg.message_id)
		except Exception as e:
			print(e)
			msg = await bot.send_message(message.chat.id, "⚠️ Такой страницы нет")
			await bot.delete_message(message.chat.id, message.message_id)
			time.sleep(3)
			await bot.delete_message(message.chat.id, msg.message_id)
	await state.finish()
	

@dp.message_handler(state = worker.idhandler)
async def idhandlerhd(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		try:
			id = int(message.text)
			await bot.edit_message_text(chat_id = message.chat.id, message_id = data["idhandler"], text = f"{editworker(message.text)}", parse_mode='HTML', disable_web_page_preview = True, reply_markup = workerkey(message.text))
			await bot.delete_message(message.chat.id, message.message_id)

		except:
			msg = await bot.send_message(message.chat.id, "⚠️ Такого ID нет")
			await bot.delete_message(message.chat.id, message.message_id)
			time.sleep(3)
			await bot.delete_message(message.chat.id, msg.message_id)
	await state.finish()

	

























@dp.message_handler(state = zayavka.first)
async def first(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		
		data['first'] = message.text
		await bot.delete_message(message.chat.id, message.message_id)
		msg = await bot.edit_message_text(chat_id = message.chat.id, message_id = data['msg'],text = f"<b>Твоя заявка: Не заполнена!\n\n1. {message.text}\n2. ⚙️ Есть ли у тебя опыт в данной сфере?</b>", parse_mode = "HTML", reply_markup = zayotmena())
		data["msg"] = msg.message_id

	await zayavka.next()

@dp.message_handler(state = zayavka.second)
async def second(message: types.Message, state: FSMContext):

	async with state.proxy() as data:

		data['second'] = message.text
		await bot.delete_message(message.chat.id, message.message_id)
		msg = await bot.edit_message_text(chat_id = message.chat.id, message_id = data['msg'],text = f"<b>Твоя заявка: Не заполнена!\n\n1. {data['first']}\n2. {message.text}\n3. 💰 Каких целей планируешь достичь вместе с нами?</b>", parse_mode = "HTML", reply_markup = zayotmena())
		data["msg"] = msg.message_id

	await zayavka.next()

@dp.message_handler(state = zayavka.third)
async def third(message: types.Message, state: FSMContext):

	async with state.proxy() as data:

		data['third'] = message.text
		await bot.delete_message(message.chat.id, message.message_id)
		await bot.edit_message_text(chat_id = message.chat.id, message_id = data['msg'],text = f"<b>Твоя заявка: Заполнена!\n\n1. {data['first']}\n2. {data['second']}\n3. {data['third']}</b>", parse_mode = "HTML", reply_markup = zaycomplete(message.chat.id))
		


executor.start_polling(dp, skip_updates = True)


