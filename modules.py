from telebot import types

import os
import pyjokes
import random
import requests
import wikipedia
import xkcd

CURRENCY_API_KEY = 'GET IT FROM https://fixer.io/'
RAPID_API_KEY = os.environ.get('RAPID_API_KEY')


def reply(bot, message, intent, entities):
    if intent == 'xkcd':
        random_comic = xkcd.getRandomComic()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Check out another xkcd comic!'))
        bot.send_photo(message.chat.id, random_comic.getImageLink(), caption='*' +
                       random_comic.getTitle() + '*\n' + random_comic.getAltText() +
                       '\n' + random_comic.getExplanation(), parse_mode='Markdown',
                       reply_to_message_id=message.message_id, reply_markup=markup)
    elif intent == 'hello':
        greetings = [
            'Hello there!',
            'Hey!',
            'Hi!',
            'Oh hello!'
        ]
        greeting = random.choice(greetings)
        bot.reply_to(message, greeting)
    elif intent == 'thanks':
        bot.reply_to(message, u'\u2764')
    elif intent == 'bye':
        greetings = [
            'Bye!',
            'Have a great day ahead!',
            'See you soon!'
        ]
        greeting = random.choice(greetings)
        bot.reply_to(message, greeting)
        gifs = [
            'https://media.giphy.com/media/UrcXN0zTfzTPi/giphy.gif',
            'https://media.giphy.com/media/3o6EhGvKschtbrRjX2/giphy.gif'
        ]
        gif = random.choice(gifs)
        bot.send_animation(message.chat.id, gif)
    elif intent == 'coin':
        coin_images = {
            'Heads': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/01/heads.png',
            'Tails': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/01/tails.png'
        }
        result = random.choice(['Heads', 'Tails'])
        bot.send_photo(message.chat.id, photo=coin_images[result],
                       reply_to_message_id=message.message_id)
    elif intent == 'dice':
        dice_images = {
            '1': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_1.png',
            '2': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_2.png',
            '3': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_3.png',
            '4': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_4.png',
            '5': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_5.png',
            '6': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_6.png'
        }
        result = random.choice(['1', '2', '3', '4', '5', '6'])
        bot.send_photo(message.chat.id, photo=dice_images[result],
                       reply_to_message_id=message.message_id)
    elif intent == 'joke':
        bot.reply_to(message, text=pyjokes.get_joke())
    elif intent == 'fact':
        response = requests.get('http://numbersapi.com/random/trivia')
        if (response.status_code == 200):
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, 'I could not fetch a fact for you this time. Please try again later!')
    elif intent == 'currency':
        amount = entities[0]['amount'][0]['value']
        from_currency = entities[0]['from_currency'][0]['value'].upper()
        to_currency = entities[0]['to_currency'][0]['value'].upper()
        r = requests.get('http://data.fixer.io/api/latest?access_key='+CURRENCY_API_KEY)
        data = r.json()
        from_rate = data['rates'][from_currency]
        to_rate = data['rates'][to_currency]
        converted = round(amount*(to_rate/from_rate),2)
        bot.reply_to(message, converted)
    elif intent == 'wiki':
        try:
            query = entities[0]['value']
            data = wikipedia.summary(query, sentences=5)
            bot.reply_to(message, data)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'I could not fetch the Wikipedia summary for you this time. Please try again later!')
    elif intent == 'dictionary':
        word = entities[0]['value']
        response = requests.get('https://wordsapiv1.p.rapidapi.com/words/' + word + '/definitions', headers={
            'x-rapidapi-key': RAPID_API_KEY
        })
        data = response.json()
        if (response.status_code == 200):
            bot.reply_to(message, data['definitions'][0]['definition'])
        else:
            bot.reply_to(message, data['message'])
    elif intent == 'anime':
        anime = entities[0]['value']
        response = requests.get('https://jikan1.p.rapidapi.com/search/anime', headers={
            'x-rapidapi-key': RAPID_API_KEY
        }, params={
            'q': anime
        })
        data = response.json()
        bot.send_photo(message.chat.id, data['results'][0]['image_url'], caption='*' + data['results'][0]['title'] + '*\n' + data['results'][0]['synopsis'] + '\n\nRating: ' + str(data['results'][0]['score']) + '\nNumber of episodes: ' + str(data['results'][0]['episodes']),
                       parse_mode='Markdown', reply_to_message_id=message.message_id)
    elif intent == 'meme':
        response = requests.get('https://meme-api.herokuapp.com/gimme/memes')
        if (response.status_code == 200):
            data = response.json()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Check out another meme!'))
            bot.send_photo(message.chat.id, data['url'], caption='*' + data['title'] + '*', parse_mode='Markdown',
                           reply_to_message_id=message.message_id, reply_markup=markup)
        else:
            bot.reply_to(message, 'I could not fetch a meme for you this time. Please try again later!')
    elif intent == 'help':
        help_message = """Hi there! I'm Jarvis, your personal assistant.\n\nYou can tell me things like:
- show me a xkcd comic
- flip a coin
- roll a dice
- tell me a joke
- define server
- cloud wiki
- death note anime
\nI'm always learning, so do come back and say hi from time to time! Have a nice day. 🙂"""
        bot.reply_to(message, help_message)
    else:
        title = "Unhandled+query:+" + message.text
        body = "What's+the+expected+result?+PLACEHOLDER_TEXT"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Report', url="https://github.com/the-vision/jarvis-telegram/issues/new?title=" + title + "&body=" + body))
        bot.send_message(message.chat.id, text="Sorry, this feature isn't available yet!",
                         parse_mode='Markdown', reply_to_message_id=message.message_id, reply_markup=markup)
