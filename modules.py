from telebot import types
import xkcd
import random


def reply(bot, message, intent, entities):
    if intent == 'xkcd':
        random_comic = xkcd.getRandomComic()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Check out another xkcd comic!'))
        bot.send_photo(message.chat.id, random_comic.getImageLink(), caption='*' +
                       random_comic.getTitle() + '*\n' + random_comic.getAltText() +
                       '\n' + random_comic.getExplanation(), parse_mode='Markdown',
                       reply_to_message_id=message.message_id, reply_markup=markup)

    if intent == 'hello':
        reply = ['hello there !', 'hey', 'hi !', 'oh hello !']
        text = random.choice(reply)
        bot.send_message(message.chat.id, text,
                       reply_to_message_id=message.message_id)
                       
    else:
        bot.reply_to(message, message.text)
