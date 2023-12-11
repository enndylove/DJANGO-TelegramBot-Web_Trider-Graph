# DJANGO | TelegramBot - Web Trider Graph <img src="https://img.shields.io/static/v1?label=🤖 Telegram Bot&message=Trider Graph 📈&color=4201ff" />

![](https://i.ibb.co/TH0v0Hz/image.jpg)

## Papar Information

- Title: `DJANGO | TelegramBot - Web Trider Graph`
- Authors: [`enndylove`](https://github.com/enndylove)
- Screenshot: [`Desktop / Laptop`](https://i.ibb.co/942nMCc/2023-12-10-181100.png) | [`Mobile`](https://i.ibb.co/XDCrvqh/2023-12-10-181525989.png)

# How is this project used?

\***\*First, install all the packages using the command\*\***

```
pip install -r requirements.txt
```

### Create .env file in path: /

\***\*Create your own telegram bot in BotFather, and request a token from it\*\***

```
Insert it in the file .env in the variable TOKEN
And in the file /static/bot/config.py in the variable TOKEN
```

\***\*Now you need to migrate the Django project\*\***

```
python manage.py migrate
```

\***\*You need to create 3 databases according to [.env.example](https://github.com/enndylove/DJANGO-TelegramBot-Web_Trider-Graph/.env.example)\*\***

`PATH FOR DATABASES: /static/bot/database.db`

`PATH FOR COINBASE: /static/bot/coinbase.db`

`PATH FOR WORKERBASE: /static/bot/workerbase.db`

**ALL DATABASES IN DIRECTORY: [/static/bot/](https://github.com/enndylove/DJANGO-TelegramBot-Web_Trider-Graph/static/bot/)**

```
You must have DIRECT links to the databases as long as the database is not on a branch server. Example: C:/YOUR/PATH/TO/DATABASE.db . Direct links should be changed in such files as:
- /main/views.py
- /static/bot/config.py
```

`Tables for .db files:`

```
database - tables: "req" and "users"
coinbase - tables: "coins"
workerbase - tablss: "workers"
```

\***\*After all actions, you need to start the server\*\***

```
python manage.py runserver
```

# About the project

`This project is closely related to skam.`

```
For this project, the customer sent me the Telegram bot code, the front-end part, and described what exactly my work consists of.
The customer said that other programmers gave a deadline of 1-3 months with an estimate of $1,000. I completed this project in less than 5 days.
```

### Why did I call this project a scam?

With a certain command, the Telegram bot gives you a link to your chat ID. With a certain command, the Telegram bot gives you a link to your chat ID. You will have your link, which will have a status (displayed in the console)

And I was given 3 databases of bot telegrams, workers, currency, users. The point was that I had to make 3 statuses for users and workers,

```
status 0 - random values of the graph relative to (-2 ; 2), status 1 - winning, i.e. if a person with status 1 bet on downgrade, the graph will go down, the same goes for promotion, status 2 is a loss, i.e.
```

`if a person with status 2 bets on a decrease, the graph will go up with a small interval, usually status 2 and 0 were used for users.` I had to take this status in the database, in relation to the Telegram bot (of course, I informed the customer that he needed a separate server for the database, but at the moment I did it directly from the file), `in which the "senior" could select a user and put his status`, then the database was changing, so I made it so that the database was updated every time the page was loaded. I also had to make sure that each user had his own page. Change the frontend, and a couple more exercises

### How did I do it?

To begin with, I read the code of the bot's telegrams, read what is contained in the databases, read the entire code `(about 50,000 lines)`, it was difficult to understand what was to what, because I was analyzing someone else's code, which was written very awkwardly, not broken down into blocks, not formed After that I realized that it would be best to write it in django, I rewrote all the code in django so that I could work both with python (on which the telegram bot is written) and to work with html. After that, I made my own page for each user using the chat ID from the user database (this database was taken from the Telegram bot, which, when pressing the start button, recorded all the necessary information in the database, and recorded default data for unknown information).

```
YOU WILL NOT BE ABLE TO USE THE WEB PAGE WITHOUT A CHAT ID THAT IS IN YOUR DATABASE. That is, the path to the page should look something like this: https://YOUR_HOST/658257014.
```

I made all the edits to the order. I made a status function for each user, and my own page
But since this is a scam project, I was also not deceived when I did the work in 5 days, and when it came to payment, I was paid 1/4 of the promised amount, and they said that this is silence. Of course, I am also a person with a conscience, and I did not drain the database with 164 users in a human way.

## Code Details

### Function for status:

- **Status 0**: Raindom integer, min 25 000, max 35 000. Сase (-2, 2)
- **Status 1**: Win, min 25 000, max 35 000. If the user chose to increase the schedule, the chances: (-2, 2.35)
- **Status 2**: Loss, min 25 000, max 35 000. If the user chose to increase the schedule, the chances: (-2.35, 2)

![](https://i.ibb.co/VYy4tRB/2023-12-11-111025.png)

## Packages

- **_All packages in a file: [requirements.txt](https://github.com/enndylove/DJANGO-TelegramBot-Web_Trider-Graph/requirements.txt)_**

## Hardware

```
CPU: Intel Core i5-9300HF 2.40Ghz
GPU: Nvidia GTX1660 Ti (6GB)
```

## Directory Hierarchy

```
|—— main
    |—— admin.py
    |—— apps.py
    |—— migrations
    |    |—— __init__.py
    |—— models.py
    |—— tests.py
    |—— urls.py
    |—— views.py
    |—— __init__.py

|—— SecondDVNZ
    |—— asgi.py
    |—— settings.py
    |—— urls.py
    |—— wsgi.py
    |—— __init__.py

|—— static
    |—— app.js
    |—— bootstrap
    |    |—— * bootstrap-files *
    |—— bot
    |    |—— bot.py
    |    |—— config.py
    |    |—— defs.py
    |    |—— keyboards.py
    |    |—— languages.py
    |    |—— reloadcurs.py
    |    |—— start.bat
    |    |—— starttest.bat
    |    |—— test.html
    |    |—— test.py
    |    |—— zaybot.py
    |—— Chart.js
    |—— chartjs-plugin-annotation.min.js
    |—— img
    |    |—— *.png
    |    |—— *.svg
    |—— jquery-3.6.1.min.js
    |—— pngwing.png
    |—— popper.min.js
    |—— style.css

|—— templates
    |—— main
    |    |—— index.html

|—— .env.example
|—— .gitignore
|—— manage.py
|—— README.md
```

# License

#### This project is licensed under the [MIT License](https://github.com/enndylove/DJANGO-TelegramBot-Web_Trider-Graph/LICENCE.md).

---

# Delicious coffee to you friends ☕
