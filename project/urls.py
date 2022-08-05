from django.contrib import admin
from django.urls import path

from meetup_db import views

urlpatterns = [
    path('', admin.site.urls),
    path('admin/', admin.site.urls),
]
