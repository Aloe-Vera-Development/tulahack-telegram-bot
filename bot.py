from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import logging

# db_call.py
import db_call
import utility_custom
import get_token

import json
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

token = get_token.get_token() # function which returns token string
updater = Updater(token,
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Enter the text you want to show to the user whenever they start the bot")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("Your Message")

def login(update: Update, context: CallbackContext):
    user_id = 1
    login="thevladoss"
    password="qwerty12345"
    telegram_id=str(update.message.from_user.id)
    rc = db_call.auth(login, password, telegram_id)
    if (rc):
        update.message.reply_text("Вы авторизованы!")
    else:
        update.message.reply_text("Произошла ошибка :(")

def routine(update: Update, context: CallbackContext):
#    user_id = json.dumps(update)
    telegram_id=str(update.message.from_user.id)
    response = db_call.getEventsForUser(telegram_id)
    if (not response):
        update.message.reply_text("Вы не авторизованы!")
        return
    response = utility_custom.routines_to_routine_table(response)
#    print(user_id)
    print(response)
    update.message.reply_text(response)

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Извините, я не понял вас" % update.message.text)
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Извините, командa '%s' не поддерживается" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('login', login))
updater.dispatcher.add_handler(CommandHandler('routine', routine))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filters out unknown commands
    Filters.command, unknown))
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
updater.idle()
