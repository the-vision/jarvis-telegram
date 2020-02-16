import os
import psycopg2

from flask import Flask, request

import telebot

URL = os.environ.get('HEROKU_PROJECT_URL')
TOKEN = os.environ.get('TELEGRAM_BOT_API_TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

DB = os.environ.get('DATABASE_URL')
conn = psycopg2.connect(DB, sslmode='require')


@bot.message_handler(commands=['start'])
def start(message):
    log('start', None, message.text, message.from_user.id, None)
    bot.reply_to(message, 'At your service, ' + message.from_user.first_name + '!')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


def log(intent, entities, input, sender, postback):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO logs (intent, entities, input, sender, postback) VALUES (%s, %s, %s, %s, %s)", (intent, entities, input, sender, postback));
        conn.commit()


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
