from flask import Flask, request

import json
import os
import psycopg2
import requests
import telebot

CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD'))
FALLBACK_INTENT = os.environ.get('FALLBACK_INTENT')
DB = os.environ.get('DATABASE_URL')
MIND_STONE = os.environ.get('MIND_STONE')
TOKEN = os.environ.get('TELEGRAM_BOT_API_TOKEN')
URL = os.environ.get('HEROKU_PROJECT_URL')


bot = telebot.TeleBot(TOKEN)
conn = psycopg2.connect(DB, sslmode='require')
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    log('start', None, message.text, message.from_user.id, None)
    bot.reply_to(message, 'At your service, ' + message.from_user.first_name + '!')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def process_query(message):
    response = requests.get(MIND_STONE + '/parse?q=' + message.text)
    data = extract_structured_data(response.json())
    log(data['intent'], json.dumps(data['entities']), message.text, message.from_user.id, None)
    bot.reply_to(message, message.text)


def extract_structured_data(result):
    data = {
        'intent': FALLBACK_INTENT,
        'entities': []
    }
    if result['intent']['confidence'] > CONFIDENCE_THRESHOLD:
        data['intent'] = result['intent']['name']
    for entity in result['entities']:
        if entity['confidence'] > CONFIDENCE_THRESHOLD:
            data['entities'].append({
                'name': entity['entity'],
                'value': entity['value']
            })
    return data


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
