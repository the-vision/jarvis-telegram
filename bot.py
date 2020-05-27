from flask import Flask, request
from modules import reply
from utils import extract_structured_data, log

import json
import os
import psycopg2
import requests
import settings
import telebot

DB = os.environ.get('DATABASE_URL')
MIND_STONE = os.environ.get('MIND_STONE')
TOKEN = os.environ.get('TELEGRAM_BOT_API_TOKEN')
URL = os.environ.get('HEROKU_PROJECT_URL')

bot = telebot.TeleBot(TOKEN)
conn = psycopg2.connect(DB, sslmode='require')
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    log(conn, 'start', None, message.text, message.from_user.id, None)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('show me a random xkcd comic'))
    markup.add(telebot.types.KeyboardButton('show me a meme'))
    bot.reply_to(message, 'At your service, ' + message.from_user.first_name +
                 '! 👋', reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def process_query(message):
    response = requests.get(MIND_STONE + '/parse?q=' + message.text)
    data = extract_structured_data(response.json())
    intent = data['intent']
    entities = data['entities']
    log(conn, intent, json.dumps(entities), message.text, message.from_user.id, None)
    reply(bot, message, intent, entities)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + '/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
