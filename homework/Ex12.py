import requests

from lib.base_case import BaseCase


class TestHomeWorkHeader(BaseCase):
    def test_homework_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")

        assert response.headers.get("x-secret-homework-header")

        cookie_value = self.get_header(response, "x-secret-homework-header")

        assert cookie_value == "Some secret value", "There is no 'Some secret value' in the response"
