# Generated by Django 4.0.6 on 2022-08-05 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='telegram_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Telegram ID'),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='telegram_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Telegram ID'),
        ),
    ]