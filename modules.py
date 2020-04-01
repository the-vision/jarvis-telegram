from telebot import types

import random
import xkcd


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
    elif intent == 'bye':
        greetings = [
            'Bye!',
            'have a great day ahead!',
            'See you soon!'
        ]
        greeting = random.choice(greetings)
        bot.reply_to(message, greeting)
    elif intent == 'coin':
        coin_images = {
            'Heads': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/01/heads.png',
            'Tails': 'https://www.ssaurel.com/blog/wp-content/uploads/2017/01/tails.png'
        }
        result = random.choice(['Heads', 'Tails'])
        bot.send_photo(message.chat.id, photo=coin_images[result],
                       reply_to_message_id=message.message_id)
    elif intent == 'translate':
        word = entities[0]['text']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Spanish', url="https://translate.google.co.in/#view=home&op=translate&sl=en&tl=es&text="+word)) 
        markup.add(types.InlineKeyboardButton(text='Japanese', url="https://translate.google.co.in/#view=home&op=translate&sl=en&tl=ja&text="+word)) 
        markup.add(types.InlineKeyboardButton(text='Russian', url="https://translate.google.co.in/#view=home&op=translate&sl=en&tl=ru&text="+word))      
        bot.send_message(message.chat.id,text="Translate to :", parse_mode='Markdown',
                       reply_to_message_id=message.message_id, reply_markup=markup)
    else:
        title = "Unhandled+query:+" + message.text
        body = "What's+the+expected+result?+PLACEHOLDER_TEXT"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Report', url="https://github.com/the-vision/jarvis-telegram/issues/new?title=" + title + "&body=" + body))
        bot.send_message(message.chat.id, text="Sorry, this feature isn't available yet!",
                         parse_mode='Markdown', reply_to_message_id=message.message_id, reply_markup=markup)
