from django.contrib import admin

from .models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ('group', 'time', 'title', 'event_type')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class GuestAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'speaker_id', 'guest_id', 'question', 'answer')


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name', 'position', 'organization',)


class SpeechAdmin(admin.ModelAdmin):
    list_display = ('event', 'title',)


admin.site.register(Guest, GuestAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Speech, SpeechAdmin)
