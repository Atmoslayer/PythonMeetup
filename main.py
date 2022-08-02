import os

from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram_bot import start, get_answer_name, message_handler

if __name__ == '__main__':
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(get_answer_name))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))


    updater.start_polling()
    print('Бот вышел в сеть')
    updater.idle()