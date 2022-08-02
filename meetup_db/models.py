from django.db import models
from django.contrib.auth.models import User  # https://django.fun/docs/django/ru/4.0/ref/contrib/auth/


# Про модели
# https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Models#модель_для_начинающих
# https://tutorial.djangogirls.org/ru/django_models/

class MeetupUsers(models.Model):
    ORGANIZER = 'ORG'  # Роль организатора
    SPEAKER = 'SPK'  # Роль докладчика
    VISITOR = 'USR'  # Роль посетителя

    ROLE_CHOICES = [
        (ORGANIZER, 'Organizer'),
        (SPEAKER, 'Speaker'),
        (VISITOR, 'Visitor'),
    ]

    user_name = models.ForeignKey(  # Ник пользователя, уникальное поле, используется в других моделях
        User,  # https://django.fun/docs/django/ru/4.0/ref/contrib/auth/
        null=False,
        on_delete=models.CASCADE,
    )
    user_role = models.CharField(  # Роль пользователя, Поле с выбором значения из ROLE_CHOICES
        max_length=3,
        choices=ROLE_CHOICES,  # https://docs.djangoproject.com/en/2.2/ref/models/fields/#choices
        default=VISITOR,
    )
