from django.contrib import admin

from .models import Group, Guest, Event, Speech, Speaker


class EventAdmin(admin.ModelAdmin):
    list_display = ('group', 'time', 'title', 'event_type')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class GuestAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name')


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'organization',)


class SpeechAdmin(admin.ModelAdmin):
    list_display = ('event', 'title',)


admin.site.register(Event, EventAdmin)
admin.site.register(Group)
admin.site.register(Guest)
admin.site.register(Speech, SpeechAdmin)
admin.site.register(Speaker, SpeakerAdmin)
