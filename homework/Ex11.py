import requests

from lib.base_case import BaseCase


class TestHomeWorkCookie(BaseCase):
    def test_homework_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie_value = self.get_cookie(response, "HomeWork")
        assert cookie_value == "hw_value", "There is no 'hw_value' in the response"
