from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from time import strftime
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()
DATABASE_PATH = os.environ.get('DATABASE_PATH')

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена</h1>")


def main(request, chat_id):
    chapters = list("eqwert")
    sqliteConnection = sqlite3.connect(DATABASE_PATH)
    cursor = sqliteConnection.cursor()

    print("Connected to SQLite")

    sqlite_select_query = """SELECT * from SqliteDb_developers"""
    cursor.execute(
        "SELECT status FROM users WHERE id = ?", (chat_id,))
    records = cursor.fetchall()
    print(records[0])
    return render(request, "main/index.html", {"chat_id": chat_id, "direction": records[0][0]})
