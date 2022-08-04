import requests


LOCALHOST ='http://127.0.0.1:8000'


def get_user(telegram_id: int) -> dict:
    global LOCALHOST

    page = 'user'
    url = f'{LOCALHOST}/{page}/{telegram_id}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        user_notes = response.json()
    except requests.exceptions.HTTPError:
        user_notes = {
            'telegram_id': None,
            'name': None,
            'surname': None,
            'role': None
        }

    return user_notes


if __name__ == '__main__':
    test_id = {
        'Dima': 1293129176,
        'Nikolai': 393728401,
        'Vasiliy': 554347536,
        'Ivan': 111,
        'Null': 0  # Пользователь отсутствует

    }

    print(f'''
    {get_user(test_id['Dima'])}
    {get_user(test_id['Nikolai'])}
    {get_user(test_id['Vasiliy'])}
    {get_user(test_id['Ivan'])}
    {get_user(test_id['Null'])}
    ''')