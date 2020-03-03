from telebot import types

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
    elif message.text == 'help':
        help_message = """Hi there! I'm Jarvis, your personal assistant.\nYou can tell me things like:
                        \n - trending news
                        \n - motivate me
                        \n - whats the weather like in Chennai?
                        \n - gold price
                        \n - show a random xkcd comic
                        \n - make me laugh
                        \nI'm always learning, so do come back and say hi from time to time!\nHave a nice day. 🙂"""
        bot.reply_to(message, (help_message))
    else:
        bot.reply_to(message, message.text)
