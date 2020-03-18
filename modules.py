from telebot import types

import pyjokes
import random
import requests
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
        bot.send_animation(message.chat.id, 'https://media.giphy.com/media/UrcXN0zTfzTPi/giphy.gif')
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
    else:
        title = "Unhandled+query:+" + message.text
        body = "What's+the+expected+result?+PLACEHOLDER_TEXT"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Report', url="https://github.com/the-vision/jarvis-telegram/issues/new?title=" + title + "&body=" + body))
        bot.send_message(message.chat.id, text="Sorry, this feature isn't available yet!",
                         parse_mode='Markdown', reply_to_message_id=message.message_id, reply_markup=markup)
