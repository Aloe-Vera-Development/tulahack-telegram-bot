from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters


#buttons
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from telegram import Bot
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
bot = Bot(token)
updater = Updater(token,
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Пожалуйста, авторизуйтесь в системе с помощью команды  `/login name pass`")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я твой помощник в уходе за растениями - @seedcare_bot")

def login(update: Update, context: CallbackContext):
    login, password = utility_custom.parse_args(update.message.text, 2)
    #login="thevladoss"
    #password="qwerty12345"
    telegram_id=str(update.message.from_user.id)
    rc = db_call.auth(login, password, telegram_id)
    if (rc):
        update.message.reply_text("Вы авторизованы!")
    else:
        update.message.reply_text("Произошла ошибка :(")

def btn(name, id):
    name = "Выполнить " + str(name)
    id = "/complete " + str(id)
    return InlineKeyboardButton(name, callback_data=id)

def routine(update: Update, context: CallbackContext):
#    user_id = json.dumps(update)
    telegram_id=str(update.message.from_user.id)
    response = db_call.getEventsForUser(telegram_id)
    print(response)
    try:
        if len(response) == 1 and len(response[0]) == 0:
            update.message.reply_text("Все сделано! Вы хорошо потрудились.")
            return
    except TypeError:
        if (not response):
            update.message.reply_text("Пусто!")
            return
    response_text = utility_custom.routines_to_routine_table(response)
#    print(user_id) 
    keyboard = [[btn(task[0] + str(task[3]), str(task[3]))] for task in response]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(response_text, reply_markup=reply_markup)

def complete(update: Update, context:  CallbackContext):
    source = update.callback_query.data 
    task_id = utility_custom.parse_args(source, 1)[0]
    rc = db_call.complete(task_id)
    print(f"complete({rc})")
    if (rc):
        bot.answerCallbackQuery(update.callback_query.id, "Задание выполнено!")
        # routine(update,context)
    else:
        bot.answerCallbackQuery(update.callback_query.id, "Такого задания нет  :(")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Извините, я не понял вас" % update.message.text)
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Извините, командa '%s' не поддерживается" % update.message.text)

def callback_query_handler(update: Update, context: CallbackContext):
    complete(update, context)


updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('login', login))
updater.dispatcher.add_handler(CommandHandler('routine', routine))
updater.dispatcher.add_handler(CommandHandler('complete', complete))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filters out unknown commands
    Filters.command, unknown))
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
updater.idle()
