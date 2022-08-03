# Generated by Django 4.0.6 on 2022-08-03 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_db', '0005_alter_meetupusers_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetupusers',
            name='user_role',
            field=models.CharField(choices=[('ORG', 'Organizer'), ('VST', 'Visitor'), ('SPK', 'Speaker')], default='VST', max_length=3),
        ),
    ]
