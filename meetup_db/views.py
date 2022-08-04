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

    print('REQUEST USER:', context)

    return JsonResponse(context)


def create_user(request):
    params = request.GET
    params = params.dict()
    add_user = MeetupUsers(
        telegram_id = params['telegram_id'],
        user_name = params.setdefault('name', 'Коллега'),
        user_surname = params.get('surname'),
        user_role = params.setdefault('role', 'VST')
    )
    add_user.save()

    print('ADD USER:', add_user)


    return user_detail(request, add_user.telegram_id)
