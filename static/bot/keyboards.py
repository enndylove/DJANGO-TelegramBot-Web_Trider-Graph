from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import supportname, site, admins, rusogl, uasogl, egsogl, database, workerbase
from languages import *
import sqlite3


def setslang():

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "🇬🇧 English", callback_data = "setslang eg")
	btn2 = InlineKeyboardButton(text = "🇺🇦 Українська", callback_data = "setslang ua")
	btn3 = InlineKeyboardButton(text = "🇷🇺 Русский", callback_data = "setslang ru")

	markup.row(btn1).row(btn2).row(btn3)

	return markup

def sogl(lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = Language.langf(lang).kbsogl, callback_data = "prinsogl")
	markup.row(btn)

	return markup

def startkb(lang, id):

	markup = ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)
	btn1 = KeyboardButton(Language.langf(lang).kbmenu4)
	btn2 = KeyboardButton(Language.langf(lang).kbstart)
	btn3 = KeyboardButton(Language.langf(lang).kbmenu5)
	btn4 = KeyboardButton(Language.langf(lang).kbmenu6)

	markup.row(btn1).row(btn2).row(btn3, btn4)

	con = sqlite3.connect(workerbase)
	cur = con.cursor()
	cur.execute("SELECT id FROM workers WHERE id = ?", (id,))
	worker = cur.fetchone()

	if str(id) in admins:
		btn5 = KeyboardButton("🤴 Админ")
		markup.row(btn5)
	else:
		if worker != None:
			btn5 = KeyboardButton("👷🏿‍♂️ Панель воркера")
			markup.row(btn5)


	

	return markup

def menukb(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = Language.langf(lang).kbmenu1, callback_data = "popoln")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbmenu2, callback_data = "vivod")
	btn3 = InlineKeyboardButton(text = Language.langf(lang).kbmenusite, url = site)
	btn4 = InlineKeyboardButton(text = Language.langf(lang).kbmenu3, callback_data = "settings")
	
	markup.row(btn1, btn2).row(btn4)

	return markup

def helpkb(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = Language.langf(lang).kbhelp1, url = f"http://t.me/{supportname}")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn1).row(btn2)

	return markup

def closekb(lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn)

	return markup

def settingskb(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = Language.langf(lang).kbsettings1, callback_data = "setvalut")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbsettings2, callback_data = "setlang")
	btn3 = InlineKeyboardButton(text = Language.langf(lang).kbsettings3, callback_data = "verification")
	btn4 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn1).row(btn2).row(btn3).row(btn4)

	return markup

def setvalut(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "🇪🇺 EUR", callback_data = "setvalut2 EUR")
	btn2 = InlineKeyboardButton(text = "🇺🇸 USD", callback_data = "setvalut2 USD")
	btn3 = InlineKeyboardButton(text = "🇺🇦 UAH", callback_data = "setvalut2 UAH")
	btn4 = InlineKeyboardButton(text = "🇵🇱 PLN", callback_data = "setvalut2 PLN")
	btn5 = InlineKeyboardButton(text = "🇷🇺 RUB", callback_data = "setvalut2 RUB")
	btn6 = InlineKeyboardButton(text = "🇧🇾 BYN", callback_data = "setvalut2 BYN")
	btn7 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn1, btn2).row(btn3, btn4).row(btn5, btn6).row(btn7)

	return markup

def setsvalut():

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "🇪🇺 EUR", callback_data = "setsvalut EUR")
	btn2 = InlineKeyboardButton(text = "🇺🇸 USD", callback_data = "setsvalut USD")
	btn3 = InlineKeyboardButton(text = "🇺🇦 UAH", callback_data = "setsvalut UAH")
	btn4 = InlineKeyboardButton(text = "🇵🇱 PLN", callback_data = "setsvalut PLN")
	btn5 = InlineKeyboardButton(text = "🇷🇺 RUB", callback_data = "setsvalut RUB")
	btn6 = InlineKeyboardButton(text = "🇧🇾 BYN", callback_data = "setsvalut BYN")

	markup.row(btn1, btn2).row(btn3, btn4).row(btn5, btn6)
	return markup

def setlang(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "🇬🇧 English", callback_data = "setlang2 eg")
	btn2 = InlineKeyboardButton(text = "🇺🇦 Українська", callback_data = "setlang2 ua")
	btn3 = InlineKeyboardButton(text = "🇷🇺 Русский", callback_data = "setlang2 ru")
	btn4 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn1).row(btn2).row(btn3).row(btn4)

	return markup

def verifkb(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = Language.langf(lang).kbverif, url = f"http://t.me/{supportname}")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn1).row(btn2)

	return markup

def infokb(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = Language.langf(lang).kbhelp1, url = f"http://t.me/{supportname}")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbinfo2, url = f"http://t.me/{supportname}")
	btn3 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn1).row(btn2).row(btn3)

	return markup

def popolnkb(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = Language.langf(lang).kbpopoln1, callback_data = "popolncard")
	btn2 = InlineKeyboardButton(text = "🌐 Paysend", callback_data = "popolnpaysend")
	btn3 = InlineKeyboardButton(text = Language.langf(lang).kbpopoln2, callback_data = "popolncrypto BTC")
	btn4 = InlineKeyboardButton(text = Language.langf(lang).kbpopoln3, callback_data = "popolncrypto ETH")
	btn5 = InlineKeyboardButton(text = Language.langf(lang).kbpopoln4, callback_data = "popolncrypto USDT")
	btn6 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn1).row(btn2).row(btn3).row(btn4).row(btn5).row(btn6)

	return markup

def popolnwor(id, summ):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "✔️", callback_data = f"popolnit {id} {summ}")
	btn2 = InlineKeyboardButton(text = "✖️", callback_data = "close")

	markup.row(btn1, btn2)

	return markup

def vivodwor(id, summ):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "✔️", callback_data = f"vivodwor {id} {summ}")
	btn2 = InlineKeyboardButton(text = "✖️", callback_data = "close")

	markup.row(btn1, btn2)

	return markup

def vivodkb(lang):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = Language.langf(lang).kbotmenavivod, callback_data = "otmenavivod")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbpopoln1, callback_data = "vivodcard")
	btn3 = InlineKeyboardButton(text = Language.langf(lang).kbpopoln2, callback_data = "vivodcrypto")
	btn4 = InlineKeyboardButton(text = Language.langf(lang).kbpopoln3, callback_data = "vivodcrypto")
	btn5 = InlineKeyboardButton(text = Language.langf(lang).kbpopoln4, callback_data = "vivodcrypto")
	btn6 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn1).row(btn2).row(btn3).row(btn4).row(btn5).row(btn6)

	return markup

def tradingkb(lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "❓FAQ", callback_data = "FAQ")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbtrade1, callback_data = "crypto")
	btn3 = InlineKeyboardButton(text = Language.langf(lang).kbtrade2, callback_data = "companies")
	btn4 = InlineKeyboardButton(text = Language.langf(lang).kbclose, callback_data = "close")

	markup.row(btn).row(btn2, btn3).row(btn4)

	return markup

def companieskb(lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "Amazon", callback_data = "token Amazon")
	btn2 = InlineKeyboardButton(text = "Tesla", callback_data = "token Tesla")
	btn3 = InlineKeyboardButton(text = "Apple", callback_data = "token Apple")
	btn4 = InlineKeyboardButton(text = "Google", callback_data = "token Google")
	btn5 = InlineKeyboardButton(text = "Microsoft", callback_data = "token Microsoft")
	btn6 = InlineKeyboardButton(text = Language.langf(lang).kbback, callback_data = "trading")

	markup.row(btn, btn2).row(btn3, btn4).row(btn5).row(btn6)

	return markup

def cryptokb(lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "Bitcoin", callback_data = "token Bitcoin")
	btn2 = InlineKeyboardButton(text = "Ethereum", callback_data = "token Ethereum")
	btn3 = InlineKeyboardButton(text = "Binance", callback_data = "token Binance")
	btn4 = InlineKeyboardButton(text = "DogeCoin", callback_data = "token DogeCoin")
	btn5 = InlineKeyboardButton(text = "Matic", callback_data = "token Matic")
	btn6 = InlineKeyboardButton(text = "Solana", callback_data = "token Solana")
	btn7 = InlineKeyboardButton(text = "Ada", callback_data = "token Ada")
	btn8 = InlineKeyboardButton(text = "Litecoin", callback_data = "token Litecoin")
	btn9 = InlineKeyboardButton(text = "Fil", callback_data = "token Fil")
	btn10 = InlineKeyboardButton(text = "Cardano", callback_data = "token Cardano")
	btn11 = InlineKeyboardButton(text = Language.langf(lang).kbback, callback_data = "trading")

	markup.row(btn, btn2).row(btn3, btn4).row(btn5, btn6).row(btn7, btn8).row(btn9, btn10).row(btn11)

	return markup

def futureskb(token, lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = Language.langf(lang).kbfut1, callback_data = f"token {token}")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbfut2, callback_data = f"futures long {token}")
	btn3 = InlineKeyboardButton(text = Language.langf(lang).kbfut3, callback_data = f"futures short {token}")
	btn4 = InlineKeyboardButton(text = Language.langf(lang).kbback, callback_data = "trading")

	markup.row(btn).row(btn2).row(btn3).row(btn4)

	return markup

def positionkb(info, lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = Language.langf(lang).kbpos1, callback_data = f"time 10 {info[0]} {info[1]} {info[2]} {info[3]} {info[4]}")
	btn2 = InlineKeyboardButton(text = Language.langf(lang).kbpos2, callback_data = f"time 30 {info[0]} {info[1]} {info[2]} {info[3]} {info[4]}")
	btn3 = InlineKeyboardButton(text = Language.langf(lang).kbpos3, callback_data = f"time 60 {info[0]} {info[1]} {info[2]} {info[3]} {info[4]}")
	btn4 = InlineKeyboardButton(text = Language.langf(lang).kbback, callback_data = "trading")

	markup.row(btn, btn2, btn3).row(btn4)

	return markup

def resultkb(lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = Language.langf(lang).kbback, callback_data = "trading")

	markup.row(btn)

	return markup

def back(lang):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = Language.langf(lang).kbotmena, callback_data = "close")

	markup.row(btn)

	return markup

def adminkb():

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "ℹ️ Инфа ℹ️", callback_data = "admininfo")
	btn2 = InlineKeyboardButton(text = "💳 Реквизиты 💳", callback_data = "requisites")
	btn3 = InlineKeyboardButton(text = "📝 Список юзеров 🧑‍💻", callback_data = "listmamonts")
	btn4 = InlineKeyboardButton(text = "📀 Обновить курсы 📀", callback_data = "reloadkurses")
	btn5 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn).row(btn2, btn3).row(btn4).row(btn5)

	return markup

def workerkb():

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "ℹ️ Инфа ℹ️", callback_data = "workerinfo")
	btn2 = InlineKeyboardButton(text = "💠 Реф.ссылка 💠", callback_data = "refka")
	btn3 = InlineKeyboardButton(text = "💸 Лимиты 💸", callback_data = "limits")
	btn4 = InlineKeyboardButton(text = "🔉 Рассылка 🔉", callback_data = "totalspam")
	btn5 = InlineKeyboardButton(text = "📝 Мамонты 🦣", callback_data = "listmamonts")
	btn6 = InlineKeyboardButton(text = "🗑 Удалить всех мамонтов 🦣", callback_data = "delallmam")
	btn7 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn).row(btn2).row(btn3).row(btn4).row(btn5).row(btn6).row(btn7)

	return markup

def workback():

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "🔙 Отмена 🔙", callback_data = "close")

	markup.row(btn)

	return markup


def setrequisiteskb():

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "🇪🇺 EUR", callback_data = "setrequisites EUR")
	btn2 = InlineKeyboardButton(text = "🇺🇸 USD", callback_data = "setrequisites USD")
	btn3 = InlineKeyboardButton(text = "🇺🇦 UAH", callback_data = "setrequisites UAH")
	btn4 = InlineKeyboardButton(text = "🇵🇱 PLN", callback_data = "setrequisites PLN")
	btn5 = InlineKeyboardButton(text = "🇷🇺 RUB", callback_data = "setrequisites RUB")
	btn6 = InlineKeyboardButton(text = "🇧🇾 BYN", callback_data = "setrequisites BYN")
	btn7 = InlineKeyboardButton(text = "🪙 BTC", callback_data = "setrequisites BTC")
	btn8 = InlineKeyboardButton(text = "🪙 ETH", callback_data = "setrequisites ETH")
	btn9 = InlineKeyboardButton(text = "🪙 USDT", callback_data = "setrequisites USDT")
	btn10 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn1, btn2).row(btn3, btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)

	return markup


def yesdel():

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "👌 Да, удалить🗑", callback_data = "yesdelallmam")
	btn2 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn).row(btn2)

	return markup

def yesdelone(id, msg_id):

	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "👌 Да, удалить 🗑", callback_data = f"yesdelmam {id} {msg_id}")
	btn2 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn).row(btn2)

	return markup

def mamonts(message, page):
	con = sqlite3.connect(database)
	cur = con.cursor()

	if str(message.chat.id) in admins:
		cur.execute("SELECT id, name FROM users")
		id = reversed(cur.fetchall())

	else:
		cur.execute("SELECT id, name FROM users WHERE boss = ?",(message.chat.id,))
		id = reversed(cur.fetchall())

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
				btn = InlineKeyboardButton(text=id[1], callback_data=f"mamont {id[0]}")
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
	btn4 = InlineKeyboardButton(text='♻️ Обновить ♻️',callback_data = "reloadmamontslist")
	btn5 = InlineKeyboardButton(text='Ввести ид', callback_data = "idhandler")
	btn6 = InlineKeyboardButton(text='❌ Закрыть ❌',callback_data = "close")
	markup.row(btn1, btn2, btn3).row(btn4).row(btn5).row(btn6)


	return markup


def userkey(id):

	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "♻️ Обновить ♻️", callback_data = f"reloaduserinfo {id}")
	btn2 = InlineKeyboardButton(text = "🏳️ Проигрыш", callback_data = f"stat loss {id}")
	btn3 = InlineKeyboardButton(text = "🎲 Рандом", callback_data = f"stat rand {id}")
	btn4 = InlineKeyboardButton(text = "👑 Выигрыш", callback_data = f"stat win {id}")
	btn5 = InlineKeyboardButton(text = "✔️ Верификация ✖️", callback_data = f"verifimam {id}")
	btn6 = InlineKeyboardButton(text = "🔄 Сменить баланс", callback_data = f"smenabal {id}")
	btn7 = InlineKeyboardButton(text = "➕ Пополнить баланс", callback_data = f"addbalance {id}")
	btn8 = InlineKeyboardButton(text = "💲 Мин.пополнение", callback_data = f"minpopoln {id}")
	btn9 = InlineKeyboardButton(text = "💲 Мин.вывод", callback_data = f"minvivod {id}")
	btn10 = InlineKeyboardButton(text = "✍️ Написать ✍️", callback_data = f"writemamont {id}")
	btn11 = InlineKeyboardButton(text = "📥 Присвоить 🦣", callback_data = f"mymam {id}")
	btn12 = InlineKeyboardButton(text = "🗑 Удалить 🦣", callback_data = f"delmam {id}")
	btn13 = InlineKeyboardButton(text = "🔒 Вывод", callback_data = f"blockvivod {id}")
	btn14 = InlineKeyboardButton(text = "🔒 Трейд", callback_data = f"blocktrade {id}")
	btn15 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn1).row(btn2, btn3, btn4).row(btn5).row(btn6, btn7).row(btn8, btn9).row(btn10).row(btn11, btn12).row(btn13, btn14).row(btn15)

	return markup

def refkakb(botname, id):
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text = "BitMart 💠 Margin", url = f"http://t.me/{botname}?start={id}")

	markup.row(btn)

	return markup

def workerlimitskb():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "💲 Мин.пополнение 💲", callback_data = "setlimit minpopoln")
	btn2 = InlineKeyboardButton(text = "💲 Мин.вывод 💲", callback_data = "setlimit minvivod")
	btn3 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn1).row(btn2).row(btn3)

	return markup

def workerlimitskb2(action):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text = "🇪🇺 EUR", callback_data = f"setworklimit EUR {action}")
	btn2 = InlineKeyboardButton(text = "🇺🇸 USD", callback_data = f"setworklimit USD {action}")
	btn3 = InlineKeyboardButton(text = "🇺🇦 UAH", callback_data = f"setworklimit UAH {action}")
	btn4 = InlineKeyboardButton(text = "🇵🇱 PLN", callback_data = f"setworklimit PLN {action}")
	btn5 = InlineKeyboardButton(text = "🇷🇺 RUB", callback_data = f"setworklimit RUB {action}")
	btn6 = InlineKeyboardButton(text = "🇧🇾 BYN", callback_data = f"setworklimit BYN {action}")
	btn7 = InlineKeyboardButton(text = "❌ Закрыть ❌", callback_data = "close")

	markup.row(btn1, btn2, btn3).row(btn4, btn5, btn6).row(btn7)

	return markup