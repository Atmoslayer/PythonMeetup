from django.contrib import admin
from django.urls import path

from meetup_db import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', views.create_user),
    path('groups/<int:group_id>', views.get_groups),
    path('events/', views.get_events),
    path('user/<int:telegram_id>', views.user_detail),
]
