from django.db import models
from django.core.exceptions import ObjectDoesNotExist

'''
Про модели
https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Models#модель_для_начинающих
https://tutorial.djangogirls.org/ru/django_models/
'''


class Group(models.Model):  # Группы Вступительные, Пото1 , Поток 2.. Заключительные
    name = models.CharField('Группа', max_length=50)

    def __str__(self):
        return self.name


class Guest(models.Model):
    telegram_id = models.IntegerField(
        'Telegram ID',
        unique=True,
        primary_key=True,
    )
    name = models.CharField('Имя', max_length=50)  # Задается в диалоге с ботом

    def __str__(self):
        return self.name


class Event(models.Model):  # Сами блоки мероприятий: Регистрация, доклад. обед, доклад итд
    SPEECH = 'SP'
    OTHER = 'OT'

    TYPE_CHOICES = [
        (SPEECH, 'Speech'),
        (OTHER, 'Other'),
    ]

    time = models.TimeField('Время начала', )
    title = models.CharField('название мероприятия', max_length=200)

    event_type = models.CharField(
        'Тип',
        max_length=2,
        choices=TYPE_CHOICES,
        default=OTHER,
    )

    group = models.ForeignKey(
        Group,
        verbose_name='группа',
        related_name='events',
        on_delete=models.CASCADE,  # наверно не надо удалять и стоит поменять
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.time}, {self.title}'


class Speech(models.Model):  # Выступление на блоке_мероприятии
    title = models.CharField('выступление', max_length=200)
    event = models.ForeignKey(
        Event,
        verbose_name='мероприятие_блок',
        related_name='speeches',
        on_delete=models.CASCADE,  # наверно не надо удалять и стоит поменять
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Speaker(models.Model):  # Все поля задаются в админке или организатором ДО мероприятия
    telegram_id = models.IntegerField(
        'Telegram ID',
        unique=True,
        primary_key=True,
    )
    name = models.CharField('Имя спикера', max_length=50)
    position = models.CharField('Должность', max_length=50)
    organization = models.CharField('Название организации', max_length=50)

    speeches_at_event = models.ManyToManyField(  # сыылка на доклады где учавствует спикер
        Speech,
        verbose_name='Выступления',
        related_name="speakers_at_speech",
    )

    def __str__(self):
        return self.name


def add_guest(user_note: dict) -> dict:
    add_guest = Guest(
        telegram_id=user_note['telegram_id'],
        name=user_note.setdefault('name', 'Коллега'),
    )
    add_guest.save()

    return get_guest(add_guest.telegram_id)


def add_speaker(user_note: dict) -> dict:
    add_speaker = Speaker(
        telegram_id=user_note['telegram_id'],
        name=user_note.setdefault('name', 'Коллега'),
        position=user_note['position'],
        organization=user_note['organization'],
        speeches_at_event=user_note['speeches_at_event'],
    )
    add_speaker.save()

    return get_speaker(add_speaker.telegram_id)


def edit_guest(user_note: dict) -> dict:
    add_user = Guest(
        telegram_id=user_note['telegram_id'],
        name=user_note.setdefault('name', 'Коллега'),
    )
    add_user.save()

    return get_guest(add_user.telegram_id)


def edit_speaker(user_note: dict) -> dict:
    add_user = Speaker(
        telegram_id=user_note['telegram_id'],
        name=user_note.setdefault('name', 'Коллега'),
    )
    add_user.save()

    return get_guest(add_user.telegram_id)


def get_events(group_id):
    button_events={}
    events = Event.objects.filter(group = group_id)
    for event in events:
        button_events[f'{event.time} {event.title}'] = event.id
    return button_events


def get_groups():
    button_groups={}
    groups = Group.objects.all()
    for group in groups:
        button_groups[group.name] = group.id
    return button_groups


def get_guest(telegram_id: int) -> dict:
    try:
        user = Guest.objects.get(telegram_id=telegram_id)
    except ObjectDoesNotExist:
        return {}

    user_note = {
        'telegram_id': user.telegram_id,
        'name': user.name,
        'role': 'GUEST'
    }

    return user_note


def get_speaker(telegram_id: int) -> dict:
    try:
        user = Speaker.objects.get(telegram_id=telegram_id)
    except ObjectDoesNotExist:
        return {}

    user_note = {
        'telegram_id': user.telegram_id,
        'name': user.name,
        'role': 'SPEAKER'
    }

    return user_note


def get_user_status(telegram_id: int) -> bool:

    if guest := get_guest(telegram_id):
        return guest['role']
    elif speaker := get_speaker(telegram_id):
        return speaker['role']
    else:
        return False

def get_event_discription(event_id):

    event = Event.objects.filter(id = event_id)[0]
    event_discription = f'{event.time} {event.title}\n'
    event_speeches = event.speeches.all()
    for event_speech in event_speeches:
        event_discription += f'\n{event_speech.title}\n'
        speakers = event_speech.speakers_at_speech.all()
        for speaker in speakers:
            event_discription +=f' {speaker.name}\n {speaker.position}\n {speaker.organization}\n'
    return event_discription