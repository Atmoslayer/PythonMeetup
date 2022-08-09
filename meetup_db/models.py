from django.db import models
from django.core.exceptions import ObjectDoesNotExist

'''
Про модели
https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Models#модель_для_начинающих
https://tutorial.djangogirls.org/ru/django_models/
'''


DEFAULT_POSITION = 'init'

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
    stance = models.CharField(  # Маркер для бота
        'Состояние',
        max_length=50,
        default=DEFAULT_POSITION,
        blank=True,
        null=True,
    )

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

    stance = models.CharField(  # Маркер для бота
        'Состояние',
        max_length=50,
        default=DEFAULT_POSITION,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Message(models.Model):
    speaker = models.ForeignKey(
        Speaker,
        verbose_name='ID спикера',
        related_name='questions',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
    )

    guest = models.ForeignKey(
        Guest,
        verbose_name='ID гостя',
        related_name='answers',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
    )

    question = models.TextField(
        'Вопрос',
        blank=False,
        null=False,
    )

    answer = models.TextField(
        'Ответ',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.question


def add_answer(answer_notes: dict) -> dict:
    answer = Message.objects.filter(
        speaker_id=answer_notes['speaker_id'],
        guest_id=answer_notes['guest_id'],
    )
    answer.update(answer=answer_notes['answer'])

    return answer


def add_guest(user_note: dict) -> dict:
    add_guest = Guest(
        telegram_id=user_note['telegram_id'],
        name=user_note.setdefault('name', 'Коллега'),
        stance=user_note.setdefault('stance', 'init')
    )
    add_guest.save()

    return get_guest(add_guest.telegram_id)


def add_question(question_notes: dict) -> dict:
    guest_id = question_notes['guest_id']

    if not get_guest(guest_id):
        add_speaker_to_guest(guest_id)

    message_notes = Message(
        speaker_id=question_notes['speaker_id'],
        guest_id=question_notes['guest_id'],
        question=question_notes['question'],
    )
    add_question.save()

    question = Message.objects.filter(id=add_question.id)

    return question


def add_speaker_to_guest(telegram_id: int) -> dict:
    speaker_notes = get_speaker(telegram_id)
    add_guest(speaker_notes)
    guest_notes = get_guest(telegram_id)

    return guest_notes


def delete_message(question_notes: dict) -> dict:
    msg_notes = Message.objects.get(
        speaker_id=question_notes['speaker_id'],
        guest_id=question_notes['guest_id'],
        question=question_notes['question']
    )
    msg_notes.delete()

    return msg_notes


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
    button_events = {}
    events = Event.objects.filter(group=group_id)
    for event in events:
        button_events[f'{event.time.strftime("%H:%M")} {event.title}'] = event.id
    return button_events


def get_groups():
    button_groups = {}
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
        'stance': user.stance,
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
        'stance': user.stance,
        'role': 'SPEAKER'
    }

    return user_note


def get_user_status(telegram_id: int):
    if speaker := get_speaker(telegram_id):
        return speaker['role']
    elif guest := get_guest(telegram_id):
        return guest['role']
    else:
        return False


def get_event_discription(event_id):
    event = Event.objects.filter(id=event_id)[0]
    event_discription = f'{event.time.strftime("%H:%M")} {event.title}\n'
    event_speeches = event.speeches.all()
    for event_speech in event_speeches:
        event_discription += f'\n*{event_speech.title}*\n Спикеры:\n'
        speakers = event_speech.speakers_at_speech.all()
        for speaker in speakers:
            event_discription += f' -{speaker.name}\n  {speaker.position}, {speaker.organization}\n'
    return event_discription


def get_speech_events(group_id):
    button_speech_events = {}
    speech_events = Event.objects.filter(group=group_id).filter(event_type='SP')
    for speech_event in speech_events:
        button_speech_events[f'{speech_event.time.strftime("%H:%M")} {speech_event.title}'] = speech_event.id
    return button_speech_events


def get_event_speekers(event_id):
    button_speakers = {}
    event = Event.objects.get(id=event_id)
    event_speeches = event.speeches.all()
    for event_speech in event_speeches:
        speakers = event_speech.speakers_at_speech.all()
        for speaker in speakers:
            button_speakers[f'{speaker.name} {speaker.position} {speaker.organization}'] = speaker.telegram_id

    return button_speakers


def get_questions(speaker_id: int) -> dict:
    speaker = Speaker.objects.get(telegram_id=speaker_id)
    questions = speaker.questions.values('id', 'guest', 'question')

    return questions


def get_answer(question_notes: dict) -> str:
    msg_notes = Message.objects.get(
        speaker_id=question_notes['speaker_id'],
        guest_id=question_notes['guest_id'],
        question=question_notes['question']
    )

    return msg_notes.answer

def get_user_stance(telegram_id: int):
    if speaker := get_speaker(telegram_id):
        return speaker['stance']
    elif guest := get_guest(telegram_id):
        return guest['stance']
    else:
        return False


def edit_user_stance(user_notes: dict):
    user_id = user_notes['telegram_id']

    if speaker := get_speaker(user_id):
        speaker = Speaker.objects.filter(telegram_id=user_id)
        speaker.update(stance=user_notes['stance'])

    if guest := get_guest(user_id):
        guest = Guest.objects.filter(telegram_id=user_id)
        guest.update(stance=user_notes['stance'])


    return get_user_stance(user_notes['telegram_id'])