from django.db import models


# Про модели
# https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Models#модель_для_начинающих
# https://tutorial.djangogirls.org/ru/django_models/

class MeetupUsers(models.Model):
    ORGANIZER = 'ORG'  # Роль организатора
    SPEAKER = 'SPK'  # Роль докладчика
    VISITOR = 'USR'  # Роль посетителя

    ROLE_CHOICES = {
        (ORGANIZER, 'Organizer'),
        (SPEAKER, 'Speaker'),
        (VISITOR, 'Visitor'),
    }

    user_id = models.AutoField(  # Ник пользователя или телефон, уникальное поле, используется в других моделях
        unique=True,
        primary_key=True,
    )

    user_name = models.CharField(  # Имя пользователя если есть, иначе обращение через 'Коллега'
        max_length=50,
        default='Коллега',
    )

    user_surname = models.CharField(  # Фамилия пользователя если есть, иначе None/Null
        max_length=50,
        null=True
    )

    user_role = models.CharField(  # Роль пользователя, Поле с выбором значения из ROLE_CHOICES
        max_length=3,
        choices=ROLE_CHOICES,  # https://docs.djangoproject.com/en/2.2/ref/models/fields/#choices
        default=VISITOR,
    )

    def __str__(self):
        user_note = f'{self.user_role}: {self.user_id} {self.user_name}'

        return user_note
