import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from meetup_db.models import *


if __name__ == '__main__':

    guest_1 = {
        'telegram_id': 51747500,
        'name': 'Ольга'  # Необязательный, при пустом значении ставится "Коллега"
    }

    guest_2 = {
        'telegram_id': guest_1['telegram_id'],
        'name': 'Ольга Николаевна'  # Необязательный, при пустом значении ставится "Коллега"
    }

    speaker_1 = {
        'telegram_id': 555899,
        'name': 'Сергей Петрович Шишкин',
        'position': 'DevOps Engineer',
        'organization': 'ОАО "Рубикон"',
        'speeches_at_event': '14:50:00, Автоматизация рекламных коммуникаций'  # Уже из созданных Speachs
    }

    guest_questions = {
        'speaker_id': 12,
        'guest_id': 500,
        'question': 'Когда будут следующие доклады от вас?'
    }

    speaker_answers = {
        'speaker_id': 12,
        'guest_id': 500,
        'answer': 'Тестовый ответ 1'
    }


    print('SPEAKER QUESTIONS:', get_questions(12))
    print('ADD QUESTION:', add_question(guest_questions))
    print('ADD ANSWER:', add_answer(speaker_answers))
    print('GUEST ANSWER:', get_answer(guest_questions))
    print('DELETE MESSAGE:', delete_message(guest_questions))

    """
    add_question({
        'speaker_id': 12,
        'guest_id': 500,
        'question': 'Когда будут следующие доклады от вас?'
    })

    get_questions(12) # принимает ID спикера

    add_answer({
        'speaker_id': 12,
        'guest_id': 500,
        'answer': 'Тестовый ответ 1'
    }) 

    get_answer({
        'speaker_id': 12,
        'guest_id': 500,
        'question': 'Когда будут следующие доклады от вас?'
    })  # Вернёт ответ str 
    """
