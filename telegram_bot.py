from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters

from finite_state_machine import PythonMeetupBot
from transitions import MachineError



menu_button = ['Меню']


def set_keyboards_buttons(buttons):
    keyboard = []

    for button in buttons:
        keyboard.append(KeyboardButton(button))

    return keyboard


def get_keyboard(buttons, one_time_keyboard=False):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[set_keyboards_buttons(buttons)],
        resize_keyboard=True,
        one_time_keyboard=one_time_keyboard,
    )
    return reply_markup


def start(update, context):
    global bot
    bot = PythonMeetupBot('Meetup')
    print(bot.state)
    global users_personal_data
    users_personal_data = {
        'first_name': '',
        'last_name': '',
        'id': ''
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

        # print(user["id"])
    else:
        update.message.reply_text(f'{user["first_name"]} - это Ваше имя?',
                                  reply_markup=reply_markup)


def get_answer_name(update, context):

    query = update.callback_query
    query.answer()
    message_id = query.message.message_id
    users_personal_data['id'] = update['callback_query']['message']['chat']['id']
    if query.data == '1':
        users_personal_data['first_name'] = update['callback_query']['message']['chat']['first_name']
        users_personal_data['last_name'] = update['callback_query']['message']['chat']['last_name']
        context.bot.delete_message(update.effective_chat.id, message_id)
        message = 'Добро пожаловать!'
        reply_markup = get_keyboard(menu_button)
        context.bot.sendMessage(update.effective_chat.id, text=message, reply_markup=reply_markup)


        bot.old_name()
        print(bot.state)
    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя и фамилию')
        bot.new_name()
        print(bot.state)


def message_handler(update, context):

    text = update.message.text

    if text and bot.state == 'enter_name':
        bot.name_entered()
        print(bot.state)
        users_full_name = text.split(' ')
        users_personal_data['first_name'] = users_full_name[0]
        if len(users_full_name) >= 2:
            users_personal_data['last_name'] = users_full_name[1]

    if bot.state == 'go_to_main_menu':
        reply_markup = get_keyboard(menu_button)
        message = 'Добро пожаловать!'
        update.message.reply_text(
            text=message,
            reply_markup=reply_markup,
        )

    # print(users_personal_data)