from telebot import types

import xkcd


def reply(bot, message, intent, entities):
    if intent == 'xkcd':
        random_comic = xkcd.getRandomComic()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('See Explanation', url=random_comic.getExplanation()))
        bot.send_photo(message.chat.id, random_comic.getImageLink(), caption='*' +
                       random_comic.getTitle() + '*\n' + random_comic.getAltText(),
                       parse_mode='Markdown', reply_to_message_id=message.message_id,
                       reply_markup=markup)
    else:
        bot.reply_to(message, message.text)
