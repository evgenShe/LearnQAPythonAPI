import time

import requests

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
response_token = (response1.json()["token"])
response_seconds = (response1.json()["seconds"])
assert response1.status_code == 200

data = {"token": response_token}
response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=data)
assert response2.status_code == 200
assert response2.json()["status"] == "Job is NOT ready"

time.sleep(response_seconds + 1)

response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=data)
assert response3.status_code == 200
assert response3.json()["status"] == "Job is ready"
assert response3.json()["result"] == "42"
