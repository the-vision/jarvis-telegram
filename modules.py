from telebot import types

import xkcd
import requests

def reply(bot, message, intent, entities):
    if intent == 'xkcd':
        random_comic = xkcd.getRandomComic()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Check out another xkcd comic!'))
        bot.send_photo(message.chat.id, random_comic.getImageLink(), caption='*' +
                       random_comic.getTitle() + '*\n' + random_comic.getAltText() +
                       '\n' + random_comic.getExplanation(), parse_mode='Markdown',
                       reply_to_message_id=message.message_id, reply_markup=markup)
    elif intent.lower() == 'fact':
        response = requests.get('http://numbersapi.com/random/trivia')
        if(response.status_code==200):
            bot.reply_to(message, response.content)
        else:
            bot.reply_to(message, 'Something went wrong. Try again')
    else:
        bot.reply_to(message, message.text)
