from django.http import JsonResponse

from meetup_db.models import MeetupUsers


def user_detail(request, telegram_id):
    user_note = MeetupUsers.objects.get(telegram_id=telegram_id)

    context = {
        'telegram_id': user_note.telegram_id,
        'name': user_note.user_name,
        'surname': user_note.user_surname,
        'role': user_note.user_role
    }

    return JsonResponse(context)


def create_user(request):
    context = request.GET

    return JsonResponse(context)
