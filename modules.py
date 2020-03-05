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
    else:
        title = "Add+new+module+"+message.text
        body = message.text+"+module+not+present"
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text = 'Report', url = "https://github.com/the-vision/jarvis-telegram/issues/new?title="+title+"&body="+body))    
        bot.send_message(message.chat.id,text="Sorry, this feature isn't available yet!", 
                        parse_mode='Markdown', reply_to_message_id=message.message_id, reply_markup=markup)
