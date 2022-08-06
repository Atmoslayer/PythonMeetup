import os
import django

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters

from finite_state_machine import PythonMeetupBot
from transitions import MachineError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from meetup_db.models import Group, Guest, Event, Speech, Speaker
from meetup_db.models import get_events, get_groups, get_event_discription, add_guest, get_user_status


menu_button = ['Меню']
menu_selection_buttons_for_user = ['📋Программа', '🗣Задать вопрос спикеру', '❓Мои вопросы']
menu_selection_buttons_for_organisator = ['📋Программа', '🗣Задать вопрос спикеру', '⚙Настройки', '❓Мои вопросы']
menu_selection_buttons_for_speaker = ['📋Программа', '🗣Задать вопрос спикеру', '❓Мои вопросы']
settings_buttons = ['✔Зарегистрировать спикера',
                    '✔Зарегистрировать организатора',
                    '✔Зарегистрировать мероприятие',
                    '❌Удалить спикера',
                     '❌Удалить организатора',
                     '❌Удалить мероприятие',
                    '📍Главное меню']
program_buttons = []
events_buttons = []
main_back_button = ['📍Главное меню']
back_button = ['↩Назад']


def get_pretty_keyboard(buttons, rows_quantity):
    for button in range(0, len(buttons), rows_quantity):
        yield buttons[button: button + 1]


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


def get_lists_of_buttons(buttons, rows_quantity):
    for button_number in range(0, len(buttons), rows_quantity):
        yield buttons[button_number: button_number + rows_quantity]


def get_pretty_keyboard(buttons, rows_quantity):

    reply_markup = ReplyKeyboardMarkup(
        keyboard=list(get_lists_of_buttons(buttons, rows_quantity)), resize_keyboard=True
    )
    return reply_markup


def start(update, context):
    global bot
    bot = PythonMeetupBot('Meetup')
    print(bot.state)
    global users_personal_data
    users_personal_data = {
        'name': '',
        'telegram_id': ''
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
    users_personal_data['telegram_id'] = update['callback_query']['message']['chat']['id']


    if query.data == '1':
        users_first_name = update['callback_query']['message']['chat']['first_name']
        users_last_name = update['callback_query']['message']['chat']['last_name']
        users_personal_data['name'] = users_first_name + ' ' + users_last_name
        print(add_guest(users_personal_data))
        print(users_personal_data)

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
        # Здесь можно сохранять данные пользователя

        reply_markup = get_keyboard(menu_button)
        message = 'Добро пожаловать!'
        bot.main_menu()
        print(bot.state)

    if text in ['Меню',
                '📍Главное меню'] \
            and bot.state in ['select_a_section',
                              'go_to_programs',
                              'go_to_questions',
                              'go_to_my_questions',
                              'go_to_settings']:

        # Здесь делаем запрос к БД, получаем роль пользователя
        # Здесь делаем запрос со списком вопросов для юзера и спикера
        global questions
        global role

        role = get_user_status(users_personal_data['telegram_id'])

        if role == 'GUEST':
            reply_markup = get_pretty_keyboard(menu_selection_buttons_for_user, 3)
        if role == 'SPEAKER':
            reply_markup = get_pretty_keyboard(menu_selection_buttons_for_speaker, 3)
        if role == 'ORGANISATOR':
            reply_markup = get_pretty_keyboard(menu_selection_buttons_for_organisator, 3)

        message = 'Выберите один из следующих пунктов: '
        bot.state = 'select_a_section'

    if (text == '📋Программа' or text in back_button) and (bot.state == 'select_a_section' or bot.state == 'select_program'):
        # Здесь получаем список программ
        # programs = ['⛳Вступительные мероприятия',
        #             '🏔Поток "Эверест"',
        #             '🗻Поток "Альпы"',
        #             '🏁Заключительные мероприятия',
        #             '📍Главное меню']

        global program_buttons
        global programs
        programs = get_groups()
        program_buttons = list(programs.keys())

        message = 'Наша программа'
        reply_markup = get_pretty_keyboard(program_buttons + main_back_button, 2)

        bot.state = 'go_to_programs'
        print(bot.state)

    if (text in program_buttons) and (bot.state == 'go_to_programs'):

        global events_buttons
        global events
        program_id = programs[text]
        events = get_events(program_id)
        events_buttons = list(events.keys())
        message = 'Предстоящие события'
        reply_markup = get_pretty_keyboard(events_buttons + back_button, 2)
        bot.state = 'select_program'
        print(bot.state)

    if text in back_button and bot.state == 'select_description':
        message = 'Предстоящие события'
        reply_markup = get_pretty_keyboard(events_buttons + back_button, 2)
        bot.state = 'select_program'
        print(bot.state)

    if text in events_buttons and bot.state == 'select_program':
        event_id = events[text]
        event_description = get_event_discription(event_id)
        message = event_description
        reply_markup = get_keyboard(back_button)
        bot.description_selected()
        print(bot.state)


    if text == '🗣Задать вопрос спикеру' and bot.state == 'select_a_section':
        # Здесь получаем список программ по вопросам
        programs = ['⛳Вступительные мероприятия',
                    '🏔Поток "Эверест"',
                    '🗻Поток "Альпы"',
                    '🏁Заключительные мероприятия',
                    '📍Главное меню']

        message = 'Выберите, в какой области Вы хотите задать вопрос'
        reply_markup = get_pretty_keyboard(programs, 2)

        bot.questions()
        print(bot.state)

    if text == '⚙Настройки' and bot.state == 'select_a_section' and role == 'Организатор':
        message = 'Выберите действие'
        reply_markup = get_pretty_keyboard(settings_buttons, 1)
        bot.settings()
        print(bot.state)

    if text == '❓Мои вопросы' and bot.state == 'select_a_section' and role == 'Спикер':
        questions_button = ['📍Главное меню']

        if questions:
            message = 'Список заданных Вам вопросов'
            #Добавляем вопросы в questions_button и отображаем
        else:
            message = 'Вопросов пока нет'

        reply_markup = get_pretty_keyboard(questions_button, 2)


    if message:
        update.message.reply_text(
            text=message,
            reply_markup=reply_markup,
        )