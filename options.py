import requests


LOCALHOST = 'http://127.0.0.1:8000'
def create_user():
    global LOCALHOST

    telegram_id = '1293129176'
    page = '/user/'
    params = {
        't_id': telegram_id
    }

    url = LOCALHOST + page
    print(url)


    response = requests.get(url)
    response.raise_for_status()

    print(response.json())


if __name__ == '__main__':
    create_user()
