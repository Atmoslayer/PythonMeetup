# Generated by Django 4.0.6 on 2022-08-06 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_db', '0005_rename_guest_id_message_guest_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='answer',
            field=models.TextField(blank=True, null=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='message',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='answers', to='meetup_db.guest', verbose_name='ID гостя'),
        ),
        migrations.AlterField(
            model_name='message',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='questions', to='meetup_db.speaker', verbose_name='ID спикера'),
        ),
    ]
