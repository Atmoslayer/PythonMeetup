import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from meetup_db.models import add_guest
from meetup_db.models import add_speaker
from meetup_db.models import edit_guest
from meetup_db.models import edit_speaker
from meetup_db.models import get_events
from meetup_db.models import get_groups
from meetup_db.models import get_user_status


if __name__ == '__main__':

    guest_1 = {
        'telegram_id': 51747500,
        'name': 'Olga'  # Необязательный, при пустом значении ставится "Коллега"
    }

    guest_2 = {
        'telegram_id': guest_1['telegram_id'],
        'name': 'Olga NIKOLAEVNA'  # Необязательный, при пустом значении ставится "Коллега"
    }



    speaker_1 = {
        'telegram_id': 555899,
        'name': 'Сергей Петрович Шишкин',
        'position': 'DevOps Engineer',
        'organization': 'ОАО "Рубикон"',
        'speeches_at_event': '14:50:00, Автоматизация рекламных коммуникаций'  # Уже из созданных  Speechs
    }

    print('REQUEST GUEST:', get_user_status(guest_1['telegram_id']))  # Несуществующий гость
    print('ADD GUEST:', add_guest(guest_1))
    print('REQUEST GUEST:', get_user_status(guest_1['telegram_id']))
    print('EDIT GUEST:', edit_guest(guest_2))
    print('REQUEST GUEST:', get_user_status(guest_1['telegram_id']))  # Несуществующий спикер
    print('REQUEST GUEST:', get_user_status(speaker_1['telegram_id']))  # Cуществующий спикер
    # ДОРАБОТКА print('ADD GUEST:', add_speaker(speaker_1))
    # ДОРАБОТКА print('REQUEST GUEST:', get_user_status(speaker_1['telegram_id']))


