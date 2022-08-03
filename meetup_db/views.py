from django.shortcuts import render
from meetup_db.models import MeetupUsers

from django.http import JsonResponse

def user_detail(request):
    print(request)
    #all_users = MeetupUsers.objects.get(telegram_id=telegram_id)
    all_users = MeetupUsers.objects.all()
    print(all_users)

    context = {
        'user_role': f'{all_users}'
    }

    return JsonResponse(context)
