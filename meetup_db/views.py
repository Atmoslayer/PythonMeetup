from django.http import JsonResponse

from meetup_db.models import Guest, Group, Event, Speech, Speaker


def create_user(request):
    params = request.GET
    params = params.dict()
    add_user = Guest(
        telegram_id=params['telegram_id'],
        name=params.setdefault('name', 'Коллега'),
    )
    add_user.save()

    print('ADD USER:', add_user)

    return user_detail(request, add_user.telegram_id)


def get_groups(request):
    button_groups = []
    groups = Group.objects.all()
    for group in groups:
        button = [group.name, group.id]
        button_groups.append(button)
    return button_groups


def get_events(request, group_id):
    button_events = []
    events = Event.objects.filter(group=group_id)
    for event in events:
        button = [f'{event.time} {event.title}', event.id]
        button_events.append(button)
    return button_events


def speacer_detail(request, telegram_id):
    user_note = Guest.objects.get(telegram_id=telegram_id)

    context = {
        'telegram_id': user_note.telegram_id,
        'name': user_note.user_name
    }

    print('REQUEST USER:', context)

    return JsonResponse(context)


def user_detail(request, telegram_id):
    user_note = Guest.objects.get(telegram_id=telegram_id)

    context = {
        'telegram_id': user_note.telegram_id,
        'name': user_note.name
    }

    print('REQUEST USER:', context)

    return JsonResponse(context)
