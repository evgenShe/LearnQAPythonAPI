from json.decoder import JSONDecodeError
import requests

payload = {"name": "User"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
parsed_response_text = response.json()
print(parsed_response_text)

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)

try:
    parsed_response_text = response.json()
    print(parsed_response_text)
except JSONDecodeError:
    print("Response is not a JSON format")

response = requests.post("https://playground.learnqa.ru/api/check_type")
print(response.status_code)

response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=False)
print(response.status_code)

response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
first_response = response.history[0]
second_response = response
print(first_response.url)
print(second_response.url)

headers = {"some_headers": "123"}
response = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=headers)
print(response.text)
print(response.headers)

payload = {"login": "secret_login", "password": "secret_pass"}
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)
print(response.text)
print(response.status_code)
print(response.cookies)
print(response.headers)

cookie_value = response1.cookies.get('auth_cookie')

cookies = {}
if cookies is not None:
    cookies.update({'auth_cookie': cookie_value})

response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
print(response2.text)

# print(json.dumps(obj, indent=4))
