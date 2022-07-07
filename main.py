import validators
import re
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "5321068795:AAFr-e10PnTfOJaHtbOkXkDgBfJPP6x5UbI"
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def validate(url):
    if not validators.url(url):
        return 0
    rq = requests.get(url)
    if rq.status_code == 200:
        return 1
    else:
        return 2

def clean(text):
    if text[:5] == "https":
        text = text[8:]
    elif text[:4] == "http":
        text = text[7:]

    text = text.replace("/", "")
    return text


def shorter(update, context):
    chat_id = update.message.from_user.id
    url = update.message.text
    url = clean(url)

    rq = requests.post("http://tinyurl.com/api-create.php?url="+url)

    update.message.reply_text(rq.text)
    print(rq)


def user(update):
    update.message.reply_text(update.message.text)



def get(update: Update, bot: CallbackContext):
    try:
        userMessage = update.message.text
        if validate(userMessage) == 0:
            update.message.reply_text("Error")
        elif validate(userMessage) == 1:
            update.message.reply_text(shorter(userMessage))
        else:
            update.message.reply_text("Error")
    except:
        update.message.reply_text("Send valid link!")

    user(update)


get_handler = MessageHandler((Filters.text), user)
dispatcher.add_handler(get_handler)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send link to shortening!")


def stop(update: Update, context: CallbackContext):
    update.message.reply_text("Done!")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Any help?")


def main() -> None:

    updater = Updater("5321068795:AAFr-e10PnTfOJaHtbOkXkDgBfJPP6x5UbI")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, shorter))
    dispatcher.add_handler(CommandHandler('stop', stop))
    dispatcher.add_handler(CommandHandler('help', help))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
