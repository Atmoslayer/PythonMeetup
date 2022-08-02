from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters


def start(update, context):
    global users_personal_data
    users_personal_data = {
        'first_name': '',
        'last_name': '',
        'phone_number': ''
    }

    user = update.message.from_user

    reply_markup = ReplyKeyboardRemove()
    if user["last_name"]:
        update.message.reply_text(
            text=f'Привет, {user["first_name"]} {user["last_name"]}!',
            reply_markup=reply_markup,
        )
    else:
        update.message.reply_text(
            text=f'Привет, {user["first_name"]}!',
            reply_markup=reply_markup,
        )
    keyboard = [
        [
            InlineKeyboardButton("Да, моё", callback_data='1'),
            InlineKeyboardButton("Нет, изменить", callback_data='2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Это ваше имя?', reply_markup=reply_markup)


def get_answer_name(update, context):
    global users_data, has_enter_name

    query = update.callback_query
    query.answer()
    if query.data == '1':
        query.edit_message_text(text='Добро пожаловать!')
        users_personal_data['first_name'] = update['callback_query']['message']['chat']['first_name']
        users_personal_data['last_name'] = update['callback_query']['message']['chat']['last_name']
    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя')
        has_enter_name = True