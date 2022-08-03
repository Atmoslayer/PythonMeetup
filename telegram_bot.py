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
    update.message.reply_text(
        text='Здравствуйте. Это официальный бот по поддержке участников 🤖.',
        reply_markup=reply_markup,
    )
    keyboard = [
        [
            InlineKeyboardButton("Да, все верно", callback_data='1'),
            InlineKeyboardButton("Нет, изменить", callback_data='2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if user["last_name"]:
        update.message.reply_text(f'{user["first_name"]} {user["last_name"]} - это Ваши имя и фамилия?',
                                  reply_markup=reply_markup)
    else:
        update.message.reply_text(f'{user["first_name"]} - это Ваше имя?',
                                  reply_markup=reply_markup)


def get_answer_name(update, context):
    global users_data, has_enter_name

    query = update.callback_query
    query.answer()
    if query.data == '1':
        query.edit_message_text(text='Добро пожаловать!')
        users_personal_data['first_name'] = update['callback_query']['message']['chat']['first_name']
        users_personal_data['last_name'] = update['callback_query']['message']['chat']['last_name']
        get_users_phone(update, context)
    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя и фамилию')
        has_enter_name = True
        

def get_users_phone(update, context):
    global has_phone

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(str('Предоставить номер телефона'), request_contact=True)]], resize_keyboard=True)
    message = 'Предоставьте свой номер телефона'
    has_phone = True

    context.bot.sendMessage(update.effective_chat.id, message, reply_markup=reply_markup)


def message_handler(update, context):
    global sub_parameters, users_personal_data, has_enter_name, has_phone

    text = update.message.text

    if text and has_enter_name:
        has_enter_name = False
        users_full_name = text.split(' ')
        users_personal_data['first_name'] = users_full_name[0]
        users_personal_data['last_name'] = users_full_name[1]

        get_users_phone(update, context)
    elif has_phone:
        has_phone = False

        if update.message.contact.phone_number[:1] == '+':
            users_personal_data['phone_number'] = update.message.contact.phone_number[1:]
        else:
            users_personal_data['phone_number'] = update.message.contact.phone_number

    print(users_personal_data)