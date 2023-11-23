import requests


class TestHomeWorkCookie:
    def test_homework_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(response.cookies)
        cookie = response.cookies.get("HomeWork")
        assert cookie == "hw_value", "There is no 'hw_value' in the response"
