# Generated by Django 4.0.6 on 2022-08-08 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_db', '0006_alter_message_answer_alter_message_guest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='stance',
            field=models.CharField(blank=True, default='init', max_length=50, null=True, verbose_name='Состояние'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='stance',
            field=models.CharField(blank=True, default='init', max_length=50, null=True, verbose_name='Состояние'),
        ),
    ]