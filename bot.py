import logging
import os
import sys
import requests
import telegram
from bs4 import BeautifulSoup
from datetime import datetime, date, time
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook(
            "https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(bot, update):
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text(
        "Привет, {}!\r\nЯ умею показывать расписание спортивных событий. Доступные виды спорта:\r\n/football — футбол\r\n/basketball — баскетбол\r\n/hockey — хоккей".format(update.message.from_user.first_name))


def football_handler(bot, update):
    today = str(datetime.today()).split()[0]
    url = 'https://www.championat.com/stat/football/#' + today
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = BeautifulSoup(r.text, 'html.parser')
    tournaments = html.findAll("div", {"class": "seo-results__tournament"})
    matches = html.find("div", {"class": "seo-results"}).findAll("ul")
    events = []
    for index, tournament in enumerate(tournaments):
        tournament_matches = []
        for match in matches[index].findAll("li"):
            tournament_matches.append({"title": match.a.text, "time": match.find(
                "span", {"class": "seo-results__item-date"}).text})
        events.append({"title": tournament.a.text,
                       "matches": tournament_matches})
    message = ""
    for event in events:
        message += "*" + event.get("title") + "*"
        for match in event.get("matches"):
            message += "\r\n{}. Начало: {}".format(
                match.get("title"), match.get("time"))
        message += "\r\n\r\n"
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            bot.send_message(chat_id=update.message.chat_id,
                             text=message[x:x+4096],
                             parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text=message, parse_mode=telegram.ParseMode.MARKDOWN)


def hockey_handler(bot, update):
    today = str(datetime.today()).split()[0]
    url = 'https://www.championat.com/stat/hockey/#' + today
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = BeautifulSoup(r.text, 'html.parser')
    tournaments = html.findAll("div", {"class": "seo-results__tournament"})
    matches = html.find("div", {"class": "seo-results"}).findAll("ul")
    events = []
    for index, tournament in enumerate(tournaments):
        tournament_matches = []
        for match in matches[index].findAll("li"):
            tournament_matches.append({"title": match.a.text, "time": match.find(
                "span", {"class": "seo-results__item-date"}).text})
        events.append({"title": tournament.a.text,
                       "matches": tournament_matches})
    message = ""
    for event in events:
        message += "*" + event.get("title") + "*"
        for match in event.get("matches"):
            message += "\r\n{}. Начало: {}".format(
                match.get("title"), match.get("time"))
        message += "\r\n\r\n"
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            bot.send_message(chat_id=update.message.chat_id,
                             text=message[x:x+4096],
                             parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text=message, parse_mode=telegram.ParseMode.MARKDOWN)


def basketball_handler(bot, update):
    today = str(datetime.today()).split()[0]
    url = 'https://www.championat.com/stat/basketball/#' + today
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = BeautifulSoup(r.text, 'html.parser')
    tournaments = html.findAll("div", {"class": "seo-results__tournament"})
    matches = html.find("div", {"class": "seo-results"}).findAll("ul")
    events = []
    for index, tournament in enumerate(tournaments):
        tournament_matches = []
        for match in matches[index].findAll("li"):
            tournament_matches.append({"title": match.a.text, "time": match.find(
                "span", {"class": "seo-results__item-date"}).text})
        events.append({"title": tournament.a.text,
                       "matches": tournament_matches})
    message = ""
    for event in events:
        message += "*" + event.get("title") + "*"
        for match in event.get("matches"):
            message += "\r\n{}. Начало: {}".format(
                match.get("title"), match.get("time"))
        message += "\r\n\r\n"
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            bot.send_message(chat_id=update.message.chat_id,
                             text=message[x:x+4096],
                             parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text=message, parse_mode=telegram.ParseMode.MARKDOWN)


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(
        CommandHandler("football", football_handler))
    updater.dispatcher.add_handler(
        CommandHandler("hockey", hockey_handler))
    updater.dispatcher.add_handler(
        CommandHandler("basketball", basketball_handler))

    run(updater)
