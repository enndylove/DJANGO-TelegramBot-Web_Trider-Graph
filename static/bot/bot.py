#!/usr/bin/python
# coding: utf-8
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import random
import time
from config import *
from keyboards import *
from defs import *
from reloadcurs import *
from languages import *
import traceback


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
import asyncio


banned_users = ['777']
spamrate = 0.2

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def tofixed(num, digits=0):
    return f"{num:.{digits}f}"


async def anti_flood(*args, **kwargs):

    m = args[0]
    await asyncio.sleep(1)
    banned_users.append(m.chat.id)


class FSMmoney(StatesGroup):
    popoln = State()
    vivod = State()


class FSMfutures(StatesGroup):
    position = State()


class FSMadmin(StatesGroup):
    totalspam = State()
    req = State()
    write = State()
    minpopoln = State()
    minvivod = State()
    smenabal = State()
    addbalance = State()
    pagehandler = State()
    idhandler = State()
    limits = State()


async def profile(message):

    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(
        "SELECT lang, valut, balance, vivod, trades, referals, verif, regdate FROM users WHERE id = ?", (message.chat.id,))
    info = cur.fetchone()

    cur.execute("SELECT COUNT(1) FROM users")
    users = cur.fetchone()
    if info[6] == 0:
        verif = "❌"
    elif info[6] == 1:
        verif = "✅"
    users = users[0]/10
    if users > 0:
        top = info[4] / (users/100) + info[5]/10
        if top > 100:
            top = 100
    else:
        top = 0

    time = str(message.date)[11:13]

    if int(time) >= 7 and int(time) <= 23:

        online = random.choice(range(1300, 1500))

    elif int(time) >= 0 and int(time) <= 6:

        online = random.choice(range(150, 300))

    top = f"{top:.{2}f}"

    result = f"<b>{Language.langf(info[0]).menu1}\n\n{Language.langf(info[0]).menu2} {info[2]} {info[1]}\n{Language.langf(info[0]).menu3} {info[3]} {info[1]}\n\n{Language.langf(info[0]).menu4} {verif}\n\n{Language.langf(info[0]).menu5} {info[4]}\n{Language.langf(info[0]).menu6} {top}\n{Language.langf(info[0]).menu7} {info[5]}\n\n{Language.langf(info[0]).menu8} {info[7]}\n\n{Language.langf(info[0]).menu9} {online}</b>"

    await bot.send_photo(message.chat.id, menupic, result, parse_mode="HTML", reply_markup=menukb(info[0]))

    state = dp.current_state(user=message.chat.id)
    currect_state = await state.get_state()

    if currect_state is None:
        return
    else:
        await state.finish()


@dp.message_handler(lambda message:  str(message.chat.id) in str(banned_users), state="*")
async def handle_banned(message: types.Message):

    return True


@dp.callback_query_handler(lambda call:  str(call.message.chat.id) in str(banned_users), state="*")
async def handle_banned_answer(call):

    return True


@dp.message_handler(lambda message:  str(message.chat.id) in str(admins), commands=["ban"], state=None)
async def banfunc(message: types.Message):

    try:
        user = int(message.text[5:])
        banned_users.append(user)
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("SELECT id, name FROM users WHERE id = ?", (user,))
        username = cur.fetchone()
        await bot.send_message(message.chat.id, f"{username[0]}, {username[1]} - Забанен!")

    except:
        await bot.send_message(message.chat.id, "<b>Пришли <code>/ban id</code></b>", parse_mode="HTML")


@dp.message_handler(lambda message:  str(message.chat.id) in str(admins), commands=["unban"], state=None)
async def unbanfunc(message: types.Message):

    try:
        user = int(message.text[7:])

        try:
            while True:
                banned_users.remove(user)
        except:
            pass

        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("SELECT id, name FROM users WHERE id = ?", (user,))
        username = cur.fetchone()
        await bot.send_message(message.chat.id, f"{username[0]}, {username[1]} - Разбанен!")

    except:
        await bot.send_message(message.chat.id, "<b>Пришли <code>/unban id</code></b>", parse_mode="HTML")


@dp.message_handler(lambda message: message.chat.type == "private", commands=["start"], state="*")
@dp.throttled(anti_flood, rate=spamrate)
async def welcome(message: types.Message, state: FSMContext):
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("SELECT id FROM users WHERE id = ?", (message.chat.id, ))
        user = cur.fetchone()

        if user == None:
            if len(message.text) != 6:
                try:
                    boss = int(message.text[7:])
                except:
                    boss = 0
            else:
                boss = 0

            con = sqlite3.connect(database)
            cur = con.cursor()

            cur.execute(
                f"INSERT INTO users (id, name, link, boss, regdate)"f"VALUES ({message.chat.id}, \"{message.chat.first_name}\", \"{message.chat.username}\", {boss}, \"{str(message.date)[:10]}\")")
            con.commit()

            if boss != 0:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "SELECT referals, lang FROM users WHERE id = ?", (boss,))
                info = cur.fetchone()
                referals = info[0] + 1
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "UPDATE users SET referals = ? WHERE id = ?", (referals, boss,))
                con.commit()
                con = sqlite3.connect(workerbase)
                cur = con.cursor()
                cur.execute(
                    "SELECT minpopoln, minvivod FROM workers WHERE id = ?", (boss,))
                limits = cur.fetchone()
                if limits[0] != "25 25 500 100 1000 100" or limits[1] != "25 25 500 100 1000 100":
                    con = sqlite3.connect(database)
                    cur = con.cursor()
                    cur.execute("UPDATE users SET minpopoln = ?, minvivod = ? WHERE id = ?",
                                (limits[0], limits[1], message.chat.id,))
                    con.commit()
                if message.chat.username != None:
                    userlink = f"<a href='http://t.me/{message.chat.username}'>{message.chat.full_name}</a>"
                else:
                    userlink = f"<a href='tg://user?id={message.chat.id}'>{message.chat.full_name}</a>"
                await bot.send_message(boss, f"{Language.langf(info[1]).newref}: {userlink}\n\n{Language.langf(info[1]).newref2}: {referals}", disable_web_page_preview=True, parse_mode="HTML")

            await bot.send_message(message.chat.id, "<b>💬 Choose your language\n💬 Обери свою мову\n💬 Выбери свой язык</b>", parse_mode='HTML', reply_markup=setslang())

        else:
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT lang FROM users WHERE id = ?",
                        (message.chat.id,))
            lang = cur.fetchone()[0]
            await bot.send_message(message.chat.id, Language.langf(lang).start, parse_mode="HTML", reply_markup=startkb(lang, message.chat.id))
            await profile(message)

        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("UPDATE users SET name = ?, link = ? WHERE id = ?",
                    (message.chat.first_name, message.chat.username, message.chat.id,))
        con.commit()

        con = sqlite3.connect(workerbase)
        cur = con.cursor()
        cur.execute("UPDATE workers SET name = ?, link = ? WHERE id = ?",
                    (message.chat.first_name, message.chat.username, message.chat.id,))
        con.commit()

        state = dp.current_state(user=message.chat.id)
        currect_state = await state.get_state()

        if currect_state is None:
            return
        else:
            await state.finish()
    except Exception as e:
        print(e)
        pass


@dp.message_handler(commands=['getSite'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f"http://127.0.0.1:8000/{message.from_user.id}")


@dp.callback_query_handler(lambda call: call.message.chat.type == "private", state="*")
async def answer(call, state: FSMContext):

    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("SELECT lang FROM users WHERE id = ?",
                    (call.message.chat.id,))
        lang = cur.fetchone()[0]

        if call.data[:8] == "setslang":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("UPDATE users SET lang = ? WHERE id = ?",
                        (call.data[9:], call.message.chat.id,))
            con.commit()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Language.langf(call.data[9:]).setvalut, parse_mode="HTML", reply_markup=setsvalut())

        elif call.data[:9] == "setsvalut":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("UPDATE users SET valut = ? WHERE id = ?",
                        (call.data[10:], call.message.chat.id,))
            con.commit()

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{Language.langf(lang).soglashenie} {Language.langf(lang).soglashenielink}", disable_web_page_preview=True, parse_mode="HTML", reply_markup=sogl(lang))

        elif call.data == "prinsogl":
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, Language.langf(lang).start, reply_markup=startkb(lang, call.message.chat.id))
            await profile(call.message)

        elif call.data == "settings":
            await bot.send_message(call.message.chat.id, Language.langf(lang).settings, parse_mode="HTML", reply_markup=settingskb(lang))
            await call.answer()

        elif call.data == "setvalut":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Language.langf(lang).setvalut, parse_mode="HTML", reply_markup=setvalut(lang))

        elif call.data[:9] == "setvalut2":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT valut, balance FROM users WHERE id = ?",
                        (call.message.chat.id,))
            info = cur.fetchone()
            await revalut(info[0], call.data[10:], info[1], call.message.chat.id)
            await call.answer(f"{Language.langf(lang).setvalut2} {call.data[10:]}")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await profile(call.message)

        elif call.data == "setlang":

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Language.langf(lang).setlang1, parse_mode="HTML", reply_markup=setlang(lang))

        elif call.data[:8] == "setlang2":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("UPDATE users SET lang = ? WHERE id = ?",
                        (call.data[9:], call.message.chat.id,))
            con.commit()
            lang = call.data[9:]

            await call.answer(Language.langf(lang).setlang2)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, Language.langf(lang).start, parse_mode="HTML", reply_markup=startkb(lang, call.message.chat.id))
            await profile(call.message)

        elif call.data == "verification":

            await bot.send_message(call.message.chat.id, Language.langf(lang).veriftext, parse_mode="HTML", reply_markup=verifkb(lang))
            await call.answer()

        elif call.data == "close":

            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await state.finish()

        elif call.data == "popoln":

            await bot.send_photo(call.message.chat.id, popolnpic, Language.langf(lang).popoln, parse_mode="HTML", reply_markup=popolnkb(lang))
            await call.answer()

        elif call.data[:12] == "popolncrypto":
            data = call.data.split(" ")
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(f"SELECT {data[1]}req FROM req")
            info = cur.fetchone()[0]
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "SELECT minpopoln, valut, boss FROM users WHERE id = ?", (call.message.chat.id,))
            info2 = cur.fetchone()

            try:

                minsum = int(info2[0])
            except:

                limits = info2[0].split(" ")

                if info2[1] == "EUR":
                    minsum = limits[0]
                elif info2[1] == "USD":
                    minsum = limits[1]
                elif info2[1] == "UAH":
                    minsum = limits[2]
                elif info2[1] == "PLN":
                    minsum = limits[3]
                elif info2[1] == "RUB":
                    minsum = limits[4]
                elif info2[1] == "BYN":
                    minsum = limits[5]

            if data[1] == "USDT":
                data[1] = "USDT, TRC-20"
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, f"{Language.langf(lang).popoln2} {data[1]}\n\n{Language.langf(lang).popoln3}\n\n{Language.langf(lang).popoln4} {data[1]}: <code>{info}</code>\n\n{Language.langf(lang).popoln5}\n\n{Language.langf(lang).popoln6} {minsum} {info2[1]} {Language.langf(lang).popoln7}", parse_mode="HTML", reply_markup=helpkb(lang))
            await call.answer()

            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute("SELECT id, name FROM workers WHERE id = ?",
                        (call.message.chat.id,))
            worker = cur.fetchone()

            if call.message.chat.username != None:
                userlink = f"<a href='http://t.me/{call.message.chat.username}'>{call.message.chat.full_name}</a>"
            else:
                userlink = f"<a href='tg://user?id={call.message.chat.id}'>{call.message.chat.full_name}</a>"

            if worker == None:

                con = sqlite3.connect(workerbase)
                cur = con.cursor()
                cur.execute(
                    "SELECT id, name, link FROM workers WHERE id = ?", (info2[2],))
                worker = cur.fetchone()
                if info2[2] != 0:
                    if worker != None:
                        await bot.send_message(info2[2], f"➕ Попытка пополнения\n🦣 Мамонт: {userlink}\n💰 Крипта: {data[1]}", parse_mode="HTML", disable_web_page_preview=True)

                if worker[2] != None:
                    workerlink = f"<a href='http://t.me/{worker[2]}'>{worker[1]}</a>"
                else:
                    workerlink = f"<a href='tg://user?id={worker[0]}'>{worker[1]}</a>"
                await bot.send_message(-1001697550223, f"➕ Попытка пополнения\n🦣 Мамонт: {userlink}\n💰 Крипта: {data[1]}\n👷🏿‍♂️ Воркер: {workerlink}\n🏴󠁧󠁢󠁷󠁬󠁳󠁿 New Bot", parse_mode="HTML", disable_web_page_preview=True)

        elif call.data == "popolncard":

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "SELECT minpopoln, valut FROM users WHERE id = ?", (call.message.chat.id,))
            info = cur.fetchone()

            try:

                minsum = int(info[0])
            except:

                limits = info[0].split(" ")

                if info[1] == "EUR":
                    minsum = limits[0]
                elif info[1] == "USD":
                    minsum = limits[1]
                elif info[1] == "UAH":
                    minsum = limits[2]
                elif info[1] == "PLN":
                    minsum = limits[3]
                elif info[1] == "RUB":
                    minsum = limits[4]
                elif info[1] == "BYN":
                    minsum = limits[5]

            await bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = await bot.send_message(call.message.chat.id, f"<i>{Language.langf(lang).popolncard1} {minsum} {info[1]}</i>\n\n<b>{Language.langf(lang).popolncard2}</b>", parse_mode="HTML", reply_markup=closekb(lang))

            await FSMmoney.popoln.set()
            async with state.proxy() as data:
                data["popoln"] = msg.message_id

        elif call.data == "popolnpaysend":
            data = call.data.split(" ")
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT UAHreq FROM req")
            req = cur.fetchone()[0]

            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, f"{Language.langf(lang).popolnpaysend1} <code>{req}</code>\n{Language.langf(lang).popolnpaysend2}", disable_web_page_preview=True, parse_mode="HTML", reply_markup=helpkb(lang))

        elif call.data == "vivod":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT blockvivod FROM users WHERE id = ?",
                        (call.message.chat.id,))
            vivod = cur.fetchone()[0]

            if vivod == 0:
                await bot.send_photo(call.message.chat.id, popolnpic, Language.langf(lang).vivod1, parse_mode="HTML", reply_markup=vivodkb(lang))
                await call.answer()
            else:
                await call.answer(Language.langf(lang).block)

        elif call.data == "otmenavivod":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT vivod, balance FROM users WHERE id = ?",
                        (call.message.chat.id,))
            vivod = cur.fetchone()

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("UPDATE users SET balance = ?, vivod = ? WHERE id = ?", (int(
                vivod[0]) + int(vivod[1]), 0, call.message.chat.id,))
            con.commit()

            await call.answer(Language.langf(lang).alertvivod)

        elif call.data == "vivodcrypto":

            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, Language.langf(lang).vivodcrypto, parse_mode="HTML", reply_markup=helpkb(lang))

        elif call.data == "vivodcard":

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "SELECT minvivod, valut, balance FROM users WHERE id = ?", (call.message.chat.id,))
            info = cur.fetchone()

            try:

                minsum = int(info[0])
            except:

                limits = info[0].split(" ")

                if info[1] == "EUR":
                    minsum = limits[0]
                elif info[1] == "USD":
                    minsum = limits[1]
                elif info[1] == "UAH":
                    minsum = limits[2]
                elif info[1] == "PLN":
                    minsum = limits[3]
                elif info[1] == "RUB":
                    minsum = limits[4]
                elif info[1] == "BYN":
                    minsum = limits[5]

            await bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = await bot.send_message(call.message.chat.id, f"<i>{Language.langf(lang).vivodcard1} {minsum} {info[1]}</i>\n\n<u>{Language.langf(lang).vivodcard2}</u> {info[2]} {info[1]}\n\n<b>{Language.langf(lang).vivodcard31}</b>", parse_mode="HTML", reply_markup=closekb(lang))

            await FSMmoney.vivod.set()
            async with state.proxy() as data:
                data["vivod"] = msg.message_id

        elif call.data[:8] == "popolnit":
            data = call.data.split(" ")
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "SELECT balance, lang, valut FROM users WHERE id = ?", (data[1],))
            info = cur.fetchone()
            pop = int(data[2]) + info[0]
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("UPDATE users SET balance = ? WHERE id = ?",
                        (pop, data[1],))
            con.commit()
            await bot.send_message(data[1], f"{Language.langf(info[1]).sucpopoln} {data[2]} {info[2]}!", parse_mode="HTML")
            await call.answer("☑️ Готово ☑️")
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        elif call.data[:8] == "vivodwor":
            data = call.data.split(" ")
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT lang FROM users WHERE id = ?", (data[1],))
            lang = cur.fetchone()[0]

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("UPDATE users SET vivod = ? WHERE id = ?",
                        (0, data[1],))
            con.commit()
            await bot.send_message(data[1], f"{Language.langf(lang).sucvivod}!", parse_mode="HTML")
            await call.answer("☑️ Готово ☑️")
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        elif call.data == "trading":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Language.langf(lang).trademsg, parse_mode="HTML", reply_markup=tradingkb(lang))

        elif call.data == "crypto":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Language.langf(lang).cryptomsg, parse_mode="HTML", reply_markup=cryptokb(lang))

        elif call.data == "companies":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Language.langf(lang).companiesmsg, parse_mode="HTML", reply_markup=companieskb(lang))

        elif call.data == "FAQ":
            await bot.send_message(call.message.chat.id, Language.langf(lang).faq, parse_mode="HTML", reply_markup=closekb(lang))

        elif call.data[:5] == "token":
            con = sqlite3.connect(coinbase)
            cur = con.cursor()
            cur.execute(f"SELECT {call.data[6:]} FROM coins")
            coin = float(cur.fetchone()[0])
            dv = random.choice(range(0, 300)) / 100 - 1.5
            dv2 = (coin / 100) * dv
            coin = coin + dv2
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>{Language.langf(lang).rk} {call.data[6:]}\n{Language.langf(lang).kursl} {tofixed(coin, 3)} $\n{Language.langf(lang).dvl} {tofixed(dv, 2)} %\n{Language.langf(lang).pil} {tofixed(dv2, 2)} $</b>", parse_mode="HTML", reply_markup=futureskb(call.data[6:], lang))

        elif call.data[:7] == "futures":
            data = call.data.split(" ")
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "SELECT balance, valut, blocktrade FROM users WHERE id = ?", (call.message.chat.id,))
            info = cur.fetchone()

            if info[2] == 0:

                if info[1] == "USD":
                    minp = 5
                if info[1] == "EUR":
                    minp = 5
                if info[1] == "UAH":
                    minp = 100
                if info[1] == "PLN":
                    minp = 15
                if info[1] == "RUB":
                    minp = 200
                if info[1] == "BYN":
                    minp = 10
                msg = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>{Language.langf(lang).futures1} {data[2]}, {data[1]}\n\n{Language.langf(lang).futures2} {info[0]} {info[1]}\n{Language.langf(lang).futures3} {minp} {info[1]}</b>", parse_mode="HTML", reply_markup=back(lang))
                info = info[0], info[1], minp, data[1], data[2]
                await FSMfutures.position.set()
                async with state.proxy() as data:
                    data["position"] = call, info
            else:
                await call.answer(Language.langf(lang).block)

        elif call.data[:4] == "time":
            info = call.data.split(" ")
            times = (int(info[1])/2) - 2
            con = sqlite3.connect(coinbase)
            cur = con.cursor()
            cur.execute(f"SELECT {info[5]} FROM coins")
            coin = float(cur.fetchone()[0])
            i = 0
            while i <= times:
                i = i + 1
                dv = random.choice(range(0, 300)) / 100 - 1.5
                dv2 = (coin / 150) * dv
                coin = coin + dv2
                msg = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>{Language.langf(lang).position1} \n{info[4]}, {info[5]}: {info[6]} {info[3]}\n\n{Language.langf(lang).rk} {info[5]}\n{Language.langf(lang).kursl} {tofixed(coin, 3)} $\n{Language.langf(lang).dvl} {tofixed(dv, 2)} %\n{Language.langf(lang).pil} {tofixed(dv2, 2)} $</b>", parse_mode="HTML")
                time.sleep(2)

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "SELECT status, boss, trades FROM users WHERE id = ?", (call.message.chat.id,))
            infou = cur.fetchone()

            if info[4] == "long":
                dvs = dv
                if infou[0] == 1:
                    if dvs < 0:
                        dvs = dvs - (dvs * 2)
                elif infou[0] == 2:
                    if dvs > 0:
                        dvs = dvs - (dvs * 2)
                        dv2 = dv2 - (dv2 * 2)

                if dvs < 0:
                    result = Language.langf(lang).ubl
                elif dvs > 0:
                    result = Language.langf(lang).prl
                elif dvs == 0:
                    result = Language.langf(lang).pat

            elif info[4] == "short":
                dvs = dv
                result = 0
                if infou[0] == 1:
                    if dvs > 0:
                        dvs = dvs - (dvs * 2)
                elif infou[0] == 2:
                    if dvs < 0:
                        dvs = dvs - (dvs * 2)
                        dv2 = dv2 - (dv2 * 2)

                if dvs > 0:
                    result = Language.langf(lang).ubl
                    dvs = dvs - (dvs * 2)

                elif dvs < 0 and result != Language.langf(lang).ubl:
                    result = Language.langf(lang).prl
                    dvs = dvs - (dvs * 2)

                elif dvs == 0:
                    result = Language.langf(lang).pat

            summ = tofixed(int(info[6]) * dvs)
            if float(summ) < 0 and abs(float(summ)) > int(info[6]):
                summ = 0 - int(info[6])

            balance = tofixed(float(info[2]) + float(summ), 0)
            trades = infou[2] + 1
            lasttrade = f"{info[5]}, {info[4]}: {summ} {info[3]}"
            if int(balance) < 0:
                balance = 0

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("UPDATE users SET balance = ?, trades = ?, lasttrade = ? WHERE id = ?",
                        (balance, trades, lasttrade, call.message.chat.id,))
            con.commit()

            await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f"<b>{Language.langf(lang).position2} \n{info[4]}, {info[5]}: {info[6]} {info[3]}\n\n{Language.langf(lang).rk} {info[5]}\n{Language.langf(lang).kursl} {tofixed(coin, 3)} $\n{Language.langf(lang).dvl} {tofixed(dv, 2)} %\n{Language.langf(lang).pil} {tofixed(dv2, 2)} $\n\n{result} {summ} {info[3]}</b>", parse_mode="HTML", reply_markup=resultkb(lang))
            if infou[1] != 0:
                await bot.send_message(infou[1], f"<b>📊 Позиция закрыта: {call.message.chat.first_name} \n{info[4]}, {info[5]}: {info[6]} {info[3]}\n{result} {summ} {info[3]}</b>", parse_mode="HTML", reply_markup=closekb(lang))

        elif call.data == "admininfo":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT COUNT(1) FROM users")
            users = cur.fetchone()[0]
            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute("SELECT COUNT(1) FROM workers")
            workers = cur.fetchone()[0]
            await call.answer(f"👨‍💻 Число пользователей: {users}\n👷🏿‍♂️ Число воркеров: {workers}", show_alert=True)

        elif call.data == "workerinfo":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT COUNT(1) FROM users")
            users = cur.fetchone()[0]
            cur.execute("SELECT COUNT(1) FROM users WHERE boss = ?",
                        (call.message.chat.id,))
            mamontscount = cur.fetchone()[0]
            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute("SELECT COUNT(1) FROM workers")
            workers = cur.fetchone()[0]
            await call.answer(f"👨‍💻 Число пользователей: {users}\n👷🏿‍♂️ Число воркеров: {workers}\n🦣 Число мамонтов: {mamontscount}", show_alert=True)

        elif call.data == "totalspam":
            await call.answer("⚠️ Сообщение будет отправлено всем мамонтам")
            msg = await bot.send_message(call.message.chat.id, "<b>✍️ Введи сообщение для рассылки</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.totalspam.set()

            async with state.proxy() as data:
                data["totalspam"] = call, msg.message_id

        elif call.data == "reloadkurses":
            try:
                await call.answer("⏳ Подожди")
                reloadcurs()
                msg = await bot.send_message(call.message.chat.id, "✅ Курсы обновлены")
                time.sleep(3)
                await bot.delete_message(call.message.chat.id, msg.message_id)
            except:
                msg = await bot.send_message(call.message.chat.id, "⚠️ Ошибка")
                time.sleep(3)
                await bot.delete_message(call.message.chat.id, msg.message_id)

        elif call.data == "requisites":
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT * FROM req")
            req = cur.fetchone()
            await bot.send_message(call.message.chat.id, "<b>💳 Какие реквизиты сменить?</b>", parse_mode="HTML", reply_markup=setrequisiteskb())
            await call.answer(f"Реквизиты:\n\n🇺🇦UAH: {req[0]}\n🇺🇸USD: {req[1]}\n🇪🇺EUR: {req[2]}\n🇵🇱PLN: {req[3]}\n🇧🇾BYN: {req[4]}\n🇷🇺RUB: {req[5]}", show_alert=True)

        elif call.data[:13] == "setrequisites":
            msg = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>✍️ Введи новые реквизиты</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.req.set()
            req = call.data[14:]
            async with state.proxy() as data:
                data["req"] = req, msg.message_id

        elif call.data == "listmamonts":
            await bot.send_message(call.message.chat.id, "<b>📑 Список мамонтов 🦣</b>", parse_mode="HTML", reply_markup=mamonts(call.message, 1))
            await call.answer()

        elif call.data == "reloadmamontslist":
            try:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>📑 Список мамонтов 🦣</b>", parse_mode="HTML", reply_markup=mamonts(call.message, 1))
                await call.answer("✅ Обновлено")
            except:
                await call.answer("⚠️ Изменений нет")

        elif call.data[:1] == ">":
            info = str(call.data).split(" ")
            if int(info[1]) + 1 > int(info[2]):
                page = 1
            else:
                page = int(info[1]) + 1

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>📑 Список мамонтов 🦣</b>", parse_mode="HTML", reply_markup=mamonts(call.message, page))

        elif call.data[:11] == "pagehandler":
            await call.answer(f"⚠️ Доступно страниц: {call.data[12:]}")
            msg = await bot.send_message(call.message.chat.id, "<b>📑 Введи номер странички</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.pagehandler.set()

            async with state.proxy() as data:
                data["pagehandler"] = call, msg.message_id

        elif call.data[:9] == "idhandler":
            await call.answer("⚠️ Введи ид мамонта")
            msg = await bot.send_message(call.message.chat.id, "<b>📑 Введи ID</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.idhandler.set()

            async with state.proxy() as data:
                data["idhandler"] = msg.message_id

        elif call.data[:1] == "<":
            info = str(call.data).split(" ")
            if int(info[1]) - 1 == 0:
                page = int(info[2])
            else:
                page = int(info[1]) - 1

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>📑 Список мамонтов 🦣</b>", parse_mode="HTML", reply_markup=mamonts(call.message, page))

        elif call.data == "delallmam":
            await bot.send_message(call.message.chat.id, "<b>⚠️ Удалить всех мамонтов ❔</b>", parse_mode="HTML", reply_markup=yesdel())
            await call.answer("⚠️ Подтверди удаление")

        elif call.data == "yesdelallmam":
            try:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute("UPDATE users SET boss = ? WHERE boss = ?",
                            (0, call.message.chat.id,))
                con.commit()
                await call.answer("✅ Готово")
            except Exception as e:
                print(e)
                await call.answer("⚠️ Произошла ошибка")
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        elif call.data[:6] == "mamont":
            await bot.send_message(call.message.chat.id, f"{editmamont(call.data[7:])} {call.message.date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(call.data[7:]))
            await call.answer()

        elif call.data[:4] == "stat":
            info = call.data.split(" ")
            try:
                if info[1] == "rand":
                    status = 0
                    answ = "🎲 рандом"
                elif info[1] == "win":
                    status = 1
                    answ = "👑 выигрыш"
                elif info[1] == "loss":
                    status = 2
                    answ = "🏳 проигрыш"
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "UPDATE users SET status = ? WHERE id = ?", (status, info[2],))
                con.commit()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{editmamont(info[2])} {call.message.edit_date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(info[2]))
                await call.answer(f"⚠️ Новый статус: {answ}")
            except Exception as e:
                await call.answer(f"⚠️ Новый статус: {answ}")

        elif call.data[:14] == "reloaduserinfo":
            try:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{editmamont(call.data[15:])} {call.message.edit_date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(call.data[15:]))
                await call.answer("✅ Обновлено")
            except:
                await call.answer("⚠️ Изменений нет")

        elif call.data[:9] == "verifimam":
            id = call.data[10:]
            try:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute("SELECT verif FROM users WHERE id = ?", (id,))
                verif = cur.fetchone()[0]
                if verif == 0:
                    value = 1
                    alerttext = "✅ Аккаунт верифицирован"
                elif verif == 1:
                    value = 0
                    alerttext = "❌ Верификация снята"

                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "UPDATE users SET verif = ? WHERE id = ?", (value, id,))
                con.commit()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{editmamont(id)} {call.message.edit_date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(id))
                await call.answer(alerttext)

            except:
                await call.answer("⚠️ Ошибка")

        elif call.data[:11] == "writemamont":
            await call.answer("⚠️ Сообщение будет отправлено от имент бота")
            msg = await bot.send_message(call.message.chat.id, "<b>✍️ Введи сообщение</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.write.set()
            async with state.proxy() as data:
                data["write"] = call.data[12:], msg.message_id

        elif call.data[:9] == "minpopoln":
            await call.answer("⚠️ Значение статично вне зависимости ои валюты")
            msg = await bot.send_message(call.message.chat.id, "<b>✍️ Введи значение минимального пополнения для мамонта\n(не учитывая валюты. Для сброса введи 0)</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.minpopoln.set()
            async with state.proxy() as data:
                data["minpopoln"] = call.data[10:], msg.message_id, call.message.message_id

        elif call.data[:8] == "minvivod":
            await call.answer("⚠️ Значение статично вне зависимости ои валюты")
            msg = await bot.send_message(call.message.chat.id, "<b>✍️ Введи значение минимального вывода для мамонта\n(не учитывая валюты. Для сброса введи 0)</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.minvivod.set()
            async with state.proxy() as data:
                data["minvivod"] = call.data[9:], msg.message_id, call.message.message_id

        elif call.data[:8] == "smenabal":
            await call.answer("⚠️ Баланс будет заменен на введённый")
            msg = await bot.send_message(call.message.chat.id, "<b>✍️ Введи новый баланс</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.smenabal.set()
            async with state.proxy() as data:
                data["smenabal"] = call.data[9:], msg.message_id, call.message.message_id

        elif call.data[:10] == "addbalance":
            await call.answer("⚠️ При пополнении придет уведомление")
            msg = await bot.send_message(call.message.chat.id, "<b>✍️ Введи сколько пополнить</b>", parse_mode="HTML", reply_markup=workback())
            await FSMadmin.addbalance.set()
            async with state.proxy() as data:
                data["addbalance"] = call.data[11:], msg.message_id, call.message.message_id

        elif call.data[:6] == "delmam":
            await call.answer("⚠️ Подтверди удаление")
            await bot.send_message(call.message.chat.id, "<b>🗑 Удалить мамонта?</b>", parse_mode="HTML", reply_markup=yesdelone(call.data[7:], call.message.message_id))

        elif call.data[:5] == "mymam":
            try:
                id = call.data[6:]
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute("UPDATE users SET boss = ? WHERE id = ?",
                            (call.message.chat.id, id,))
                con.commit()

                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{editmamont(id)} {call.message.edit_date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(id))
                await call.answer("✅ Мамонт присвоен")
            except:
                await call.answer("⚠️ Ошибка")

        elif call.data[:9] == "yesdelmam":
            data = call.data.split(" ")
            try:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "UPDATE users SET boss = ? WHERE id = ?", (0, data[1],))
                con.commit()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=data[2], text=f"{editmamont(data[1])} {call.message.edit_date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(data[1]))
                await call.answer("✅ Мамонт удалён")
            except:
                await call.answer("⚠️ Ошибка")
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        elif call.data == "refka":
            botname = await bot.get_me()
            await bot.send_message(call.message.chat.id, "<b>💠 BitMart is a safe and secure UK based cryptocurrency exchange with more than 190 trading pairs</b>", parse_mode="HTML", reply_markup=refkakb(botname.username, call.message.chat.id))
            await call.answer("Перешли это сообщение маонту!")

        elif call.data == "limits":
            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute(
                "SELECT minpopoln, minvivod FROM workers WHERE id = ?", (call.message.chat.id,))
            info = cur.fetchone()

            minpopoln0 = info[0].split(" ")
            minvivod0 = info[1].split(" ")

            minpopoln = f"🇪🇺 - {minpopoln0[0]} EUR\n🇺🇸 - {minpopoln0[1]} USD\n🇺🇦 - {minpopoln0[2]} UAH\n🇵🇱 - {minpopoln0[3]} PLN\n🇷🇺 - {minpopoln0[4]} RUB\n🇧🇾 - {minpopoln0[5]} BYN"
            minvivod = f"🇪🇺 - {minvivod0[0]} EUR\n🇺🇸 - {minvivod0[1]} USD\n🇺🇦 - {minvivod0[2]} UAH\n🇵🇱 - {minvivod0[3]} PLN\n🇷🇺 - {minvivod0[4]} RUB\n🇧🇾 - {minvivod0[5]} BYN"

            await bot.send_message(call.message.chat.id, f"<b>💲 Твои лимиты для новых рефералов:\n\n💸 Мин.пополнение: \n{minpopoln}\n\n💸 Мин.вывод: \n{minvivod}</b>", parse_mode="HTML", reply_markup=workerlimitskb())
            await call.answer("⚠️ Лимиты применяються только к новым рефералам")

        elif call.data[:8] == "setlimit":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>🤏 По какой валюте установить лимит?</b>", parse_mode="HTML", reply_markup=workerlimitskb2(call.data[9:]))

        elif call.data[:12] == "setworklimit":
            msg = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>✍️ Введи новый лимит</b>", parse_mode="HTML", reply_markup=closekb("ru"))
            info = call.data.split(" ")
            await FSMadmin.limits.set()
            async with state.proxy() as data:
                data["valut"] = info[1]
                data["action"] = info[2]
                data["msg"] = msg.message_id

        elif call.data[:10] == "blockvivod":
            id = call.data[11:]
            try:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute("SELECT blockvivod FROM users WHERE id = ?", (id,))
                block = cur.fetchone()[0]
                if block == 0:
                    value = 1
                    alerttext = "🔒 Вывод заблокирован"
                elif block == 1:
                    value = 0
                    alerttext = "🔓 Вывод разблокирован"

                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "UPDATE users SET blockvivod = ? WHERE id = ?", (value, id,))
                con.commit()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{editmamont(id)} {call.message.edit_date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(id))
                await call.answer(alerttext)

            except:
                await call.answer("⚠️ Ошибка ⚠️")

        elif call.data[:10] == "blocktrade":
            id = call.data[11:]
            try:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute("SELECT blocktrade FROM users WHERE id = ?", (id,))
                block = cur.fetchone()[0]
                if block == 0:
                    value = 1
                    alerttext = "🔒 Торги заблокированы"
                elif block == 1:
                    value = 0
                    alerttext = "🔓 Торги разблокированы"

                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "UPDATE users SET blocktrade = ? WHERE id = ?", (value, id,))
                con.commit()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{editmamont(id)} {call.message.edit_date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(id))
                await call.answer(alerttext)

            except:
                await call.answer("⚠️ Ошибка ⚠️")

    except Exception as e:
        error = traceback.format_exc()
        line = error[error.find("line") + 5:]
        line = line[:line.find(", in ")]
        print(f"Ошибка:\n\n{e}\n\nСтрока: {line}")


@dp.message_handler(state=None)
@dp.throttled(anti_flood, rate=spamrate)
async def menu(message: types.Message):

    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("SELECT lang FROM users WHERE id = ?", (message.chat.id,))
        lang = cur.fetchone()[0]

        if message.text == "📁 Личный кабинет" or message.text == "📁 Особистий кабінет" or message.text == "📁 Personal office":
            await profile(message)

        elif message.text == "ℹ️ Информация" or message.text == "ℹ️ Інформація" or message.text == "ℹ️ Information":
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_photo(message.chat.id, infopic, Language.langf(lang).infotext, parse_mode="HTML", reply_markup=infokb(lang))

        elif message.text == "🛠 Поддержка" or message.text == "🛠 Підтримка" or message.text == "🛠 Support":
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_photo(message.chat.id, tppic, Language.langf(lang).helptext, parse_mode="HTML", reply_markup=helpkb(lang))

        elif message.text == "💱 Торговая площадка" or message.text == "💱 Торговий майданчик" or message.text == "💱 Trading platform":
            await bot.delete_message(message.chat.id, message.message_id)

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute("SELECT blocktrade FROM users WHERE id = ?",
                        (message.chat.id,))
            trade = cur.fetchone()[0]
            if trade == 0:
                await bot.send_message(message.chat.id, Language.langf(lang).trademsg, parse_mode="HTML", reply_markup=tradingkb(lang))
            else:
                await bot.send_message(message.chat.id, f"<b>{Language.langf(lang).block}</b>", parse_mode="HTML")

        elif message.text == "🤴 Админ" and str(message.chat.id) in admins:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id, "<b>🧑‍💻 Добро пожаловать в меню админа</b>", parse_mode="HTML", reply_markup=adminkb())

        elif message.text == "👷🏿‍♂️ Панель воркера":
            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute("SELECT id FROM workers WHERE id = ?",
                        (message.chat.id,))
            worker = cur.fetchone()

            if worker != None:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "SELECT referals FROM users WHERE id = ?", (message.chat.id,))
                referals = cur.fetchone()[0]

                botinfo = await bot.get_me()
                link = f"<a href='http://t.me/{botinfo.username}?start={message.chat.id}'>💎Реф.ссылка</a>"
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.send_message(message.chat.id, f"<b>👷🏿‍♂️ Добро пожаловать в меню воркера\n🦣 Мамонты: {referals}\n{link}</b>", parse_mode="HTML", reply_markup=workerkb())

        else:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id, Language.langf(lang).error, reply_markup=startkb(lang, message.chat.id))
    except Exception as e:
        error = traceback.format_exc()
        line = error[error.find("line") + 5:]
        line = line[:line.find(", in ")]
        print(f"Ошибка:\n\n{e}\n\nСтрока: {line}")


@dp.message_handler(state=FSMmoney.popoln)
@dp.throttled(anti_flood, rate=spamrate)
async def popolnhd(message: types.Message, state: FSMContext):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(
        "SELECT valut, minpopoln, lang, boss FROM users WHERE id = ?", (message.chat.id,))
    popoln = cur.fetchone()

    try:
        text = message.text
        await bot.delete_message(message.chat.id, message.message_id)
        if len(text) >= 4 and len(text) <= 7:
            if "." in text:
                text = text.replace(".", "")
            elif "," in text:
                text = text.replace(",", "")

        text = int(text)

        if len(str(text)) >= 4:
            mtext = str(text)[:-3]+","+str(text)[-3:]
        else:
            mtext = text

        try:

            minsum = int(popoln[1])
        except:

            limits = popoln[1].split(" ")

            if popoln[0] == "EUR":
                minsum = limits[0]
            elif popoln[0] == "USD":
                minsum = limits[1]
            elif popoln[0] == "UAH":
                minsum = limits[2]
            elif popoln[0] == "PLN":
                minsum = limits[3]
            elif popoln[0] == "RUB":
                minsum = limits[4]
            elif popoln[0] == "BYN":
                minsum = limits[5]

        if text >= int(minsum):

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(f"SELECT {popoln[0]}req FROM req")
            req = cur.fetchone()[0]

            async with state.proxy() as data:
                await bot.delete_message(message.chat.id, data["popoln"])
                await bot.send_photo(message.chat.id, popolnpic, f"{Language.langf(popoln[2]).popolncard3}\n\n{Language.langf(popoln[2]).popolncard4} <code>{req}</code>\n\n{Language.langf(popoln[2]).popolncard5} <code>BIT-ZLATO:{message.chat.id}</code>\n\n{Language.langf(popoln[2]).popolncard6} {mtext} {popoln[0]} {Language.langf(popoln[2]).popolncard7} - @{supportname}", parse_mode="HTML", reply_markup=closekb(popoln[2]))
                await state.finish()

            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute("SELECT id, name FROM workers WHERE id = ?",
                        (message.chat.id,))
            worker = cur.fetchone()

            if message.chat.username != None:
                userlink = f"<a href='http://t.me/{message.chat.username}'>{message.chat.full_name}</a>"
            else:
                userlink = f"<a href='tg://user?id={message.chat.id}'>{message.chat.full_name}</a>"

            if worker == None:

                con = sqlite3.connect(workerbase)
                cur = con.cursor()
                cur.execute(
                    "SELECT id, name, link FROM workers WHERE id = ?", (popoln[3],))
                worker = cur.fetchone()
                if popoln[3] != 0:
                    if worker != None:
                        await bot.send_message(popoln[3], f"<b>➕ Попытка пополнения\n🦣 Мамонт: {userlink}\n💰 Сумма: {mtext} {popoln[0]}</b>", parse_mode="HTML", disable_web_page_preview=True, reply_markup=popolnwor(message.chat.id, text))

                if popoln[3] != 0:
                    if worker[2] != None:
                        workerlink = f"<a href='http://t.me/{worker[2]}'>{worker[1]}</a>"
                    else:
                        workerlink = f"<a href='tg://user?id={worker[0]}'>{worker[1]}</a>"
                else:
                    workerlink = "❌Не определён"
                await bot.send_message(logs_chat_id, f"<b>➕ Попытка пополнения\n🦣 Мамонт: {userlink}\n💰 Сумма: {mtext} {popoln[0]}\n👷🏿‍♂️ Воркер: {workerlink}\n🏴󠁧󠁢󠁷󠁬󠁳󠁿New Bot</b>", parse_mode="HTML", disable_web_page_preview=True)

        else:
            msg = await bot.send_message(message.chat.id, f"{Language.langf(popoln[2]).popolncard8} {minsum} {popoln[0]}", parse_mode="HTML")
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        print(e)
        msg = await bot.send_message(message.chat.id, Language.langf(popoln[2]).popolncard9, parse_mode="HTML")
        time.sleep(3)
        await bot.delete_message(message.chat.id, msg.message_id)


@dp.message_handler(state=FSMmoney.vivod)
@dp.throttled(anti_flood, rate=spamrate)
async def vivodhd(message: types.Message, state: FSMContext):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(
        "SELECT valut, minvivod, lang, boss, balance, vivod FROM users WHERE id = ?", (message.chat.id,))
    vivod = cur.fetchone()

    try:
        text = message.text
        await bot.delete_message(message.chat.id, message.message_id)
        if len(text) >= 4 and len(text) <= 7:
            if "." in text:
                text = text.replace(".", "")
            elif "," in text:
                text = text.replace(",", "")

        text = int(text)

        if len(str(text)) >= 4:
            mtext = str(text)[:-3]+","+str(text)[-3:]
        else:
            mtext = text

        try:

            minsum = int(vivod[1])
        except:

            limits = vivod[1].split(" ")

            if vivod[0] == "EUR":
                minsum = limits[0]
            elif vivod[0] == "USD":
                minsum = limits[1]
            elif vivod[0] == "UAH":
                minsum = limits[2]
            elif vivod[0] == "PLN":
                minsum = limits[3]
            elif vivod[0] == "RUB":
                minsum = limits[4]
            elif vivod[0] == "BYN":
                minsum = limits[5]

        if text >= int(minsum):
            if text <= int(vivod[4]):
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(f"SELECT {vivod[0]}req FROM req")
                req = cur.fetchone()[0]

                async with state.proxy() as data:
                    await bot.delete_message(message.chat.id, data["vivod"])
                    balance = vivod[4] - text
                    nvivod = vivod[5] + text
                    con = sqlite3.connect(database)
                    cur = con.cursor()
                    cur.execute("UPDATE users SET balance = ?, vivod = ? WHERE id = ?",
                                (balance, nvivod, message.chat.id,))
                    con.commit()
                    await bot.send_message(message.chat.id, Language.langf(vivod[2]).vivodcard3, parse_mode="HTML", reply_markup=closekb(vivod[2]))
                    await state.finish()

                con = sqlite3.connect(workerbase)
                cur = con.cursor()
                cur.execute(
                    "SELECT id, name FROM workers WHERE id = ?", (message.chat.id,))
                worker = cur.fetchone()

                if message.chat.username != None:
                    userlink = f"<a href='http://t.me/{message.chat.username}'>{message.chat.full_name}</a>"
                else:
                    userlink = f"<a `='tg://user?id={message.chat.id}'>{message.chat.full_name}</a>"

                if worker == None:

                    con = sqlite3.connect(workerbase)
                    cur = con.cursor()
                    cur.execute(
                        "SELECT id, name, link FROM workers WHERE id = ?", (vivod[3],))
                    worker = cur.fetchone()
                    if vivod[3] != 0:
                        if worker != None:
                            await bot.send_message(vivod[3], f"<b>➕ Поставил на вывод\n🦣 Мамонт: {userlink}\n💰 Сумма: {mtext} {vivod[0]}\n💰 Общий вывод: {vivod[5] + text} {vivod[0]}</b>", parse_mode="HTML", disable_web_page_preview=True, reply_markup=vivodwor(message.chat.id, text))

            else:
                msg = await bot.send_message(message.chat.id, f"{Language.langf(vivod[2]).vivodcard4}", parse_mode="HTML")
                time.sleep(3)
                await bot.delete_message(message.chat.id, msg.message_id)
        else:
            msg = await bot.send_message(message.chat.id, f"{Language.langf(vivod[2]).vivodcard5} {minsum} {vivod[0]}", parse_mode="HTML")
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)

    except:
        msg = await bot.send_message(message.chat.id, Language.langf(vivod[2]).popolncard9, parse_mode="HTML")
        time.sleep(3)
        await bot.delete_message(message.chat.id, msg.message_id)


@dp.message_handler(state=FSMfutures.position)
async def positionhd(message: types.Message, state: FSMContext):

    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT lang FROM users WHERE id = ?", (message.chat.id,))
    lang = cur.fetchone()[0]

    async with state.proxy() as data:
        info = data["position"][1]
    try:
        if int(message.text) <= info[0]:
            if int(message.text) >= info[2]:
                info = info[0], info[1], info[3], info[4], message.text
                await bot.edit_message_text(chat_id=message.chat.id, message_id=data["position"][0].message.message_id, text=Language.langf(lang).positionl1, parse_mode="HTML", reply_markup=positionkb(info, lang))
                await bot.delete_message(message.chat.id, message.message_id)
                await state.finish()
            else:

                msg = await bot.send_message(message.chat.id, f"{Language.langf(lang).positionl2} {info[2]} {info[1]}", parse_mode="HTML")
                await bot.delete_message(message.chat.id, message.message_id)
                time.sleep(3)
                await bot.delete_message(message.chat.id, msg.message_id)
        else:

            msg = await bot.send_message(message.chat.id, f"{Language.langf(lang).positionl3} {info[0]} {info[1]}", parse_mode="HTML")
            await bot.delete_message(message.chat.id, message.message_id)
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)
    except:
        msg = await bot.send_message(message.chat.id, Language.langf(lang).popolncard9, parse_mode="HTML")
        await bot.delete_message(message.chat.id, message.message_id)
        time.sleep(3)
        await bot.delete_message(message.chat.id, msg.message_id)


@dp.message_handler(state=FSMadmin.totalspam)
async def totalspamhd(message: types.Message, state: FSMContext):
    try:
        spam = message.text
        async with state.proxy() as data:
            await bot.delete_message(message.chat.id, message.message_id)
            await data["totalspam"][0].answer("📣Рассылка началась")
            await bot.delete_message(message.chat.id, data["totalspam"][1])
            await state.finish()

        con = sqlite3.connect(database)
        cur = con.cursor()
        if str(message.chat.id) in admins:
            cur.execute("SELECT id FROM users")
            id = reversed(cur.fetchall())
        else:
            cur.execute("SELECT id FROM users WHERE boss = ?",
                        (message.chat.id,))
            id = reversed(cur.fetchall())

        for id in id:
            try:
                await bot.send_message(id[0], f"{spam}")
                time.sleep(1)
            except:
                pass

    except:
        msg = await bot.send_message(message.chat.id, "⚠️ Произошла ошибка ⚠️")
        time.sleep(3)
        await bot.delete_message(message.chat.id, msg.message_id)


@dp.message_handler(state=FSMadmin.req)
async def setrequisites(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        req = data["req"][0]
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(f"UPDATE req SET {req}req = ?", (message.text,))
        con.commit()
        await bot.send_message(message.chat.id, f"Новые реквизиты {req}: {message.text}")
        await bot.delete_message(message.chat.id, data["req"][1])
        await bot.delete_message(message.chat.id, message.message_id)
    await state.finish()


@dp.message_handler(state=FSMadmin.write)
async def writemamont(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id = data["write"][0]
        try:
            if message.chat.username != None:
                userlink = f"<a href='http://t.me/{message.chat.username}'>{message.chat.full_name}</a>"
            else:
                userlink = f"<a href='tg://user?id={message.chat.id}'>{message.chat.full_name}</a>"

            await bot.send_message(logs_chat_id, f"{userlink} отправил сообщение <a href='tg://user?id={id}'>мамонту</a>\n\nСообщение:\n{message.text}", parse_mode="HTML", disable_web_page_preview=True)
            await bot.send_message(id, message.text)
            await bot.delete_message(message.chat.id, data["write"][1])
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id, "🔊 Сообщение отправлено")

        except:
            await bot.delete_message(message.chat.id, data["write"][1])
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id, "⚠️ Сообщение не отправлено. Возможно мамонт заблокировал бота")

    await state.finish()


@dp.message_handler(state=FSMadmin.pagehandler)
async def pagehandlerhd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pagei = data["pagehandler"][0].data[12:]
        try:
            if int(message.text) <= int(pagei):
                await bot.edit_message_text(chat_id=message.chat.id, message_id=data["pagehandler"][1], text="<b>📑 Список мамонтов 🦣</b>", parse_mode="HTML", reply_markup=mamonts(message, int(message.text)))
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.delete_message(message.chat.id, data["pagehandler"][0].message.message_id)
            else:
                msg = await bot.send_message(message.chat.id, "⚠️ Такой страницы нет")
                await bot.delete_message(message.chat.id, message.message_id)
                time.sleep(3)
                await bot.delete_message(message.chat.id, msg.message_id)
        except:
            msg = await bot.send_message(message.chat.id, "⚠️ Такой страницы нет")
            await bot.delete_message(message.chat.id, message.message_id)
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)
    await state.finish()


@dp.message_handler(state=FSMadmin.idhandler)
async def idhandlerhd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            id = int(message.text)
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data["idhandler"], text=f"{editmamont(message.text)} {message.edit_date}", parse_mode='HTML', disable_web_page_preview=True, reply_markup=userkey(message.text))
            await bot.delete_message(message.chat.id, message.message_id)

        except:
            msg = await bot.send_message(message.chat.id, "⚠️ Такого ID нет")
            await bot.delete_message(message.chat.id, message.message_id)
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)
    await state.finish()


@dp.message_handler(state=FSMadmin.minpopoln)
async def minpopolnhd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            id = data["minpopoln"][0]
            minpopoln = int(message.text)
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET minpopoln = ? WHERE id = ?", (minpopoln, id,))
            con.commit()
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data["minpopoln"][2], text=f"{editmamont(id)} {message.edit_date}", parse_mode="HTML", disable_web_page_preview=True, reply_markup=userkey(id))

            await bot.delete_message(message.chat.id, data["minpopoln"][1])
            await bot.delete_message(message.chat.id, message.message_id)
            msg = await bot.send_message(message.chat.id, "☑️ Готово")
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)
        except:
            msg = await bot.send_message(message.chat.id, "⚠️ Ошибка")
            await bot.delete_message(message.chat.id, message.message_id)
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)
    await state.finish()


@dp.message_handler(state=FSMadmin.minvivod)
async def minvivodhd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            id = data["minvivod"][0]
            minvivod = int(message.text)
            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET minvivod = ? WHERE id = ?", (minvivod, id,))
            con.commit()
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data["minvivod"][2], text=f"{editmamont(id)} {message.edit_date}", parse_mode="HTML", disable_web_page_preview=True, reply_markup=userkey(id))

            await bot.delete_message(message.chat.id, data["minvivod"][1])
            await bot.delete_message(message.chat.id, message.message_id)
            msg = await bot.send_message(message.chat.id, "☑️ Готово")
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)
        except:
            msg = await bot.send_message(message.chat.id, "⚠️ Ошибка")
            await bot.delete_message(message.chat.id, message.message_id)
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)
    await state.finish()


@dp.message_handler(state=FSMadmin.smenabal)
async def smenabalhd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if int(message.text) >= 0:
                id = data["smenabal"][0]
                balance = int(message.text)
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "UPDATE users SET balance = ? WHERE id = ?", (balance, id,))
                con.commit()
                await bot.edit_message_text(chat_id=message.chat.id, message_id=data["smenabal"][2], text=f"{editmamont(id)} {message.edit_date}", parse_mode="HTML", disable_web_page_preview=True, reply_markup=userkey(id))

                await bot.delete_message(message.chat.id, data["smenabal"][1])
                await bot.delete_message(message.chat.id, message.message_id)
                msg = await bot.send_message(message.chat.id, "☑️ Готово")
                time.sleep(3)
                await bot.delete_message(message.chat.id, msg.message_id)
                await state.finish()
            else:
                msg = await bot.send_message(message.chat.id, "⚠️ Ошибка")
                await bot.delete_message(message.chat.id, message.message_id)
                time.sleep(3)
                await bot.delete_message(message.chat.id, msg.message_id)
        except:
            msg = await bot.send_message(message.chat.id, "⚠️ Ошибка")
            await bot.delete_message(message.chat.id, message.message_id)
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)


@dp.message_handler(state=FSMadmin.addbalance)
async def addbalancehd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if int(message.text) > 0:
                id = data["addbalance"][0]

                addbalance = int(message.text)
                await bot.delete_message(message.chat.id, message.message_id)
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "SELECT balance, lang, valut FROM users WHERE id = ?", (id,))
                balance = cur.fetchone()
                newbalance = balance[0] + addbalance
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute(
                    "UPDATE users SET balance = ? WHERE id = ?", (newbalance, id,))
                con.commit()
                await bot.edit_message_text(chat_id=message.chat.id, message_id=data["addbalance"][2], text=f"{editmamont(id)} {message.edit_date}", parse_mode="HTML", disable_web_page_preview=True, reply_markup=userkey(id))
                await bot.send_message(id, f"{Language.langf(balance[1]).sucpopoln} {addbalance} {balance[2]}!", parse_mode="HTML")

                await bot.delete_message(message.chat.id, data["addbalance"][1])
                msg = await bot.send_message(message.chat.id, "☑️ Готово")
                time.sleep(3)
                await bot.delete_message(message.chat.id, msg.message_id)
                await state.finish()
            else:
                msg = await bot.send_message(message.chat.id, "⚠️ Ошибка")
                time.sleep(3)
                await bot.delete_message(message.chat.id, msg.message_id)
        except:
            msg = await bot.send_message(message.chat.id, "⚠️ Ошибка")
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)


@dp.message_handler(state=FSMadmin.limits)
async def limits(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            id = message.chat.id
            valut = data["valut"]
            action = data["action"]
            msg = data["msg"]
            limit = int(message.text)

            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute(f"SELECT {action} FROM workers WHERE id = ?", (id,))
            info = cur.fetchone()

            info = info[0].split(" ")

            if valut == "EUR":
                info[0] = limit
            elif valut == "USD":
                info[1] = limit
            elif valut == "UAH":
                info[2] = limit
            elif valut == "PLN":
                info[3] = limit
            elif valut == "RUB":
                info[4] = limit
            elif valut == "BYN":
                info[5] = limit

            info = f"{info[0]} {info[1]} {info[2]} {info[3]} {info[4]} {info[5]}"

            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute(
                f"UPDATE workers SET {action} = ? WHERE id = ?", (info, id,))
            con.commit()
            con = sqlite3.connect(workerbase)
            cur = con.cursor()
            cur.execute(
                "SELECT minpopoln, minvivod FROM workers WHERE id = ?", (id,))
            info = cur.fetchone()

            minpopoln0 = info[0].split(" ")
            minvivod0 = info[1].split(" ")

            minpopoln = f"🇪🇺 - {minpopoln0[0]} EUR\n🇺🇸 - {minpopoln0[1]} USD\n🇺🇦 - {minpopoln0[2]} UAH\n🇵🇱 - {minpopoln0[3]} PLN\n🇷🇺 - {minpopoln0[4]} RUB\n🇧🇾 - {minpopoln0[5]} BYN"
            minvivod = f"🇪🇺 - {minvivod0[0]} EUR\n🇺🇸 - {minvivod0[1]} USD\n🇺🇦 - {minvivod0[2]} UAH\n🇵🇱 - {minvivod0[3]} PLN\n🇷🇺 - {minvivod0[4]} RUB\n🇧🇾 - {minvivod0[5]} BYN"
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data["msg"], text=f"<b>💲 Твои лимиты для новых рефералов:\n\n💸 Мин.пополнение: \n{minpopoln}\n\n💸 Мин.вывод: \n{minvivod}</b>", parse_mode="HTML", reply_markup=workerlimitskb())

            await bot.delete_message(message.chat.id, message.message_id)

        except Exception as e:
            print(e)
            msg = await bot.send_message(message.chat.id, "⚠️ Ошибка")
            await bot.delete_message(message.chat.id, message.message_id)
            time.sleep(3)
            await bot.delete_message(message.chat.id, msg.message_id)
    await state.finish()


executor.start_polling(dp, skip_updates=True)
