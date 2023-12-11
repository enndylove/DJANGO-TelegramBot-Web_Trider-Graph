#!/usr/bin/python
# coding: utf-8
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get('TOKEN')
ADMINS_ID = os.environ.get('ADMINS_ID')
DATABASE_PATH = os.environ.get('DATABASE_PATH')
COINBASE_PATH = os.environ.get('COINBASE_PATH')
WORKERBASE_PATH = os.environ.get('WORKERBASE_PATH')

admins = ADMINS_ID

logs_chat_id = "-882134200"

supportname = "BitMartSupport_bot"
site = "https://bitzlato-trade.online/"

tppic = "https://imgur.com/a/fxsbKmT"
menupic = "https://imgur.com/a/udwNS1T"
infopic = "https://imgur.com/a/fEpetZ2"
popolnpic = "https://imgur.com/a/r0Q6coR"

database = DATABASE_PATH
coinbase = COINBASE_PATH
workerbase = WORKERBASE_PATH

rusogl = "https://telegra.ph/Polzovatelskoe-soglashenie-bota-BitMart-02-13"
uasogl = "https://telegra.ph/Polzovatelskoe-soglashenie-bota-BitMart-02-13"
egsogl = "https://telegra.ph/Polzovatelskoe-soglashenie-bota-BitMart-02-13"
