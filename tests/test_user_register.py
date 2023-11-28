from lib.base_case import BaseCase
import requests


class TestUserRegister(BaseCase):
    def test_create_user_with_existing_email(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }
        response = requests.post("https://playground.learnqa.ru/api/user", data)

        print(response.status_code)
        print(response.content)
