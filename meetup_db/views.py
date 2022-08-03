from django.shortcuts import render
from meetup_db.models import MeetupUsers

from django.http import JsonResponse

def user_detail(request, user_id):
    print(request, user_id)
    #all_users = MeetupUsers.objects.filter(user_id=user_id)
    all_users = MeetupUsers.objects.all()
    print(all_users)

    context = {
        'user_role': f'{all_users}'
    }

    return JsonResponse(context)
