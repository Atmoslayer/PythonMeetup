from django.db import models
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
        unique=True,
        primary_key=True,
    )
    name = models.CharField(max_length=50)  # Задается в диалоге с ботом

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
