from telebot import types

import xkcd
import requests
import os
NASA_API_KEY = os.environ.get('NASA_API_KEY')
nasa_url = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(NASA_API_KEY)
def reply(bot, message, intent, entities):
    if intent == 'xkcd':
        random_comic = xkcd.getRandomComic()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Check out another xkcd comic!'))
        bot.send_photo(message.chat.id, random_comic.getImageLink(), caption='*' +
                       random_comic.getTitle() + '*\n' + random_comic.getAltText() +
                       '\n' + random_comic.getExplanation(), parse_mode='Markdown',
                       reply_to_message_id=message.message_id, reply_markup=markup)
    elif intent.lower() == 'apod':
        response = requests.get(nasa_url)
        if(response.status_code==200):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Explanation', callback_data='explanation'))
            markup.add(types.InlineKeyboardButton('Date', callback_data='date'))
            markup.add(types.InlineKeyboardButton('Copyright', callback_data='copyright'))
            bot.send_photo(message.chat.id, response.json()['url'], caption= response.json()['title'],reply_to_message_id=message.message_id, reply_markup = markup)
        else:
            
            bot.reply_to(message, 'Something went wrong. Try again!')
    else:
        bot.reply_to(message, message.text)
