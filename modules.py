import xkcd


def reply(bot, message, intent, entities):
    if intent == 'xkcd':
        random_comic = xkcd.getRandomComic()
        bot.send_photo(message.chat.id, random_comic.getImageLink(), caption='*' +
                       random_comic.getTitle() + '*\n' + random_comic.getAltText() +
                       '\n' + random_comic.getExplanation(),
                       parse_mode='Markdown', reply_to_message_id=message.message_id)
    else:
        bot.reply_to(message, message.text)
