from django.contrib import admin

from .models import *


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','id')


class EventAdmin(admin.ModelAdmin):
    list_display = ('group', 'time', 'title', 'event_type')


class SpeechAdmin(admin.ModelAdmin):
    list_display = ('event', 'title')


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'organization', 'telegram_id', 'stance')


class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'stance')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'speaker_id', 'guest_id', 'question', 'answer')


admin.site.register(Guest, GuestAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Speech, SpeechAdmin)
