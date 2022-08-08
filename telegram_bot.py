import os
import django

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters
from telegram.error import BadRequest

from finite_state_machine import PythonMeetupBot
from transitions import MachineError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from meetup_db.models import Group, Guest, Event, Speech, Speaker
from meetup_db.models import get_events, get_groups, get_event_discription, \
    add_guest, get_user_status, get_speech_events, \
    get_event_speekers, get_guest, get_speaker, add_question,  get_questions, get_answer, add_answer


question_info = {}
message = []
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
speech_events_buttons = []
question_program_buttons = []
programs = []
event_speaker_buttons = []


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


def send_message(update, message, reply_markup):
    update.message.reply_text(
        text=message,
        reply_markup=reply_markup,
    )


def get_main_menu_markup():

    if role == 'GUEST':
        reply_markup = get_pretty_keyboard(menu_selection_buttons_for_user, 3)
    if role == 'SPEAKER':
        reply_markup = get_pretty_keyboard(menu_selection_buttons_for_speaker, 3)
    if role == 'ORGANISATOR':
        reply_markup = get_pretty_keyboard(menu_selection_buttons_for_organisator, 3)

    bot.state = 'select_a_section'

    return reply_markup


def get_programs_menu(option):
    global program_buttons
    global programs
    programs = get_groups()
    program_buttons = list(programs.keys())
    for program_button in program_buttons:
        if option == 'Программы':
            program_button + ' - Вопрос'
        elif option == 'Вопросы':
            program_button + ' - Вопрос'


    message = 'Наша программа'
    reply_markup = get_pretty_keyboard(program_buttons + main_back_button, 2)

    return reply_markup, message, programs


def start(update, context):
    global bot, users_personal_data, role
    bot = PythonMeetupBot('Meetup')
    print(bot.state)
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


    role = get_user_status(user['id'])
    if role:
        message = 'Выберите один из следующих пунктов: '
        reply_markup = get_main_menu_markup()
        send_message(update, message, reply_markup)

    else:

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


def get_answer_name(update, context, query):

    query.answer()
    message_id = query.message.message_id
    users_personal_data['telegram_id'] = update['callback_query']['message']['chat']['id']

    if query.data == '1':
        users_first_name = update['callback_query']['message']['chat']['first_name']
        users_last_name = update['callback_query']['message']['chat']['last_name']
        users_personal_data['name'] = users_first_name + ' ' + users_last_name
        context.bot.delete_message(update.effective_chat.id, message_id)
        message = 'Выберите один из следующих пунктов: '
        reply_markup = get_keyboard(menu_selection_buttons_for_user)
        context.bot.sendMessage(update.effective_chat.id, text=message, reply_markup=reply_markup)
        add_guest(users_personal_data)
        bot.old_name()
        print(bot.state)
    else:
        query.edit_message_text(text='Введите, пожалуйста, ваше имя и фамилию')
        bot.new_name()
        print(bot.state)


def answer_for_question(update, context, query):
    if query.data == 'answer':
        message_id = query.message.message_id
        context.bot.delete_message(update.effective_chat.id, message_id)
        message = 'Введите ответ на вопрос'
        context.bot.sendMessage(update.effective_chat.id, text=message,
                                reply_markup=ReplyKeyboardRemove())
        bot.state = 'send_answer'
        print(bot.state)
    if query.data == 'dismis':
        message_id = query.message.message_id
        context.bot.delete_message(update.effective_chat.id, message_id)
        message = 'Вопрос удалён'
        context.bot.sendMessage(update.effective_chat.id, text=message)
        # Удаление вопроса


def callback_handler(update, context):
    name_callback = ['1', '2']
    query = update.callback_query
    if query.data in name_callback:
        get_answer_name(update, context, query)
    else:
        answer_for_question(update, context, query)


def message_handler(update, context):

    text = update.message.text

    if text and bot.state == 'enter_name':
        global role
        role = 'GUEST'
        users_personal_data['name'] = text
        add_guest(users_personal_data)
        reply_markup = get_main_menu_markup()
        message = 'Выберите один из следующих пунктов: '

    if text in ['📍Главное меню'] \
            and bot.state in ['select_a_section',
                              'go_to_programs',
                              'go_to_questions',
                              'go_to_my_questions',
                              'go_to_settings']:

        global questions
        reply_markup = get_main_menu_markup()
        message = 'Выберите один из следующих пунктов: '
        bot.state = 'select_a_section'

    if (text == '📋Программа' or text in back_button) and (bot.state == 'select_a_section' or bot.state == 'select_program'):

        global programs
        reply_markup, message, programs = get_programs_menu('Программы')
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

    if (text == '🗣Задать вопрос спикеру' or text in back_button) and (bot.state == 'select_a_section' or bot.state == 'select_question'):

        global question_programs
        reply_markup, message, question_programs = get_programs_menu('Вопросы')
        bot.state = 'go_to_questions'
        print(bot.state)

    if (text in program_buttons) and (bot.state == 'go_to_questions'):

        global speech_events_buttons
        global speech_events

        question_program_id = question_programs[text]
        speech_events = get_speech_events(question_program_id)
        speech_events_buttons = list(speech_events.keys())
        message = 'Выберите время выступления'
        reply_markup = get_pretty_keyboard(speech_events_buttons + back_button, 2)
        bot.state = 'select_question'
        print(bot.state)

    if text in speech_events_buttons and bot.state == 'select_question':
        global event_speaker_buttons
        global event_speakers
        speech_event_id = speech_events[text]
        event_speakers = get_event_speekers(speech_event_id)
        event_speaker_buttons = list(event_speakers.keys())
        message = 'Выберите спикера, которому хотите задать вопрос'
        bot.question_selected()
        print(bot.state)
        reply_markup = get_pretty_keyboard(event_speaker_buttons + back_button, 1)


    if text in event_speaker_buttons and bot.state == 'select_speaker':
        global speaker_id
        speaker_id = event_speakers[text]
        speaker_info = get_speaker(speaker_id)
        message = 'Введите Ваш вопрос'
        reply_markup = ReplyKeyboardRemove()
        bot.question_asked()
        print(bot.state)

    elif text and bot.state == 'ask_question':

        global question_text
        global user_data
        question_text = text
        keyboard = [
            [
                InlineKeyboardButton("Ответить", callback_data='answer'),
                InlineKeyboardButton("Игнорировать", callback_data='dismis'),
            ]
        ]
        users_id = update['message']['chat']['id']
        user_data = get_guest(users_id)
        if not user_data:
            user_data = get_speaker(users_id)
        print(user_data)
        users_name = user_data['name']
        question_message = f'{users_name} интересуется: {text}'
        question_info['speaker_id'] = speaker_id
        question_info['question'] = question_message
        question_info['guest_id'] = users_id
        add_question(question_info)

        reply_markup_for_question = InlineKeyboardMarkup(keyboard)
        reply_markup = get_keyboard(back_button)
        bot.question_sended()
        print(bot.state)
        try:
            context.bot.sendMessage(speaker_id, text=question_message, reply_markup=reply_markup_for_question)
            message = 'Ваш вопрос отправлен'
        except BadRequest:
            message = 'Ваш вопрос не был отправлен, попробуйте позднее. Просим прощения за причинённые неудобства'


    if text in back_button and bot.state == 'select_speaker':
        message = 'Выберите нужный поток'
        reply_markup = get_pretty_keyboard(speech_events_buttons + back_button, 2)
        bot.state = 'select_question'
        print(bot.state)

    if text in back_button and bot.state == 'send_question':
        message = 'Выберите спикера, которому хотите задать вопрос'
        reply_markup = get_pretty_keyboard(event_speaker_buttons + back_button, 1)
        bot.state = 'select_speaker'
        print(bot.state)


    # if text == '⚙Настройки' and bot.state == 'select_a_section' and role == 'Организатор':
    #     message = 'Выберите действие'
    #     reply_markup = get_pretty_keyboard(settings_buttons, 1)
    #     bot.settings()
    #     print(bot.state)
    #
    # if text == '❓Мои вопросы' and bot.state == 'select_a_section' and role == 'SPEAKER':
    #     questions_button = ['📍Главное меню']
    #
    #     if questions:
    #         message = 'Список заданных Вам вопросов'
    #     else:
    #         message = 'Вопросов пока нет'
    #
    #     reply_markup = get_pretty_keyboard(questions_button, 2)
    #
    # if text == '❓Мои вопросы' and bot.state == 'select_a_section' and role == 'GUEST':
    #     questions_button = ['📍Главное меню']
    #
    #     if questions:
    #         message = 'Список заданных Вам вопросов'
    #     else:
    #         message = 'Вопросов пока нет'
    #
    #     reply_markup = get_pretty_keyboard(questions_button, 2)

    if text and bot.state == 'send_answer':

        user_id = user_data['telegram_id']
        question_data = {}

        # Добавление ответа в БД
        message = 'Спасибо, Ваш ответ отправлен'
        reply_markup = get_keyboard(['📍Главное меню'])
        bot.state = 'select_a_section'
        speaker_id = update['message']['chat']['id']
        questions = get_questions(speaker_id)
        speaker_info = get_speaker(speaker_id)
        question_data['speaker_id'] = speaker_id
        question_data['guest_id'] = user_id
        question_data['answer'] = text
        add_answer(question_data)
        answer_message = f'{speaker_info["name"]} ответил на Ваш вопрос: {question_text}. Ответ: {text}'
        context.bot.sendMessage(user_id, text=answer_message)


    if message:
        send_message(update, message, reply_markup)