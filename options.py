import requests


LOCALHOST = 'http://127.0.0.1:8000'
def create_user():
    global LOCALHOST

    page = '/user/'
    user_id = '79211820370'
    url = LOCALHOST + page + user_id


    response = requests.get(url)
    response.raise_for_status()

    print(response.json())


if __name__ == '__main__':
    create_user()
