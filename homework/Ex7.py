import requests

methods = ["GET", "POST", "PUT", "DELETE", "LEARNQA"]

# NO method for all requested methods
for k in methods:
    response = requests.request(url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                method=k)
    if k == "LEARNQA":
        continue
    print("NO method for", k, " request: ", response.text)

# All methods for all requested methods
for i in methods:
    for j in methods:
        payload = {"method": j}
        if i == "GET":
            response = requests.request(url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        method=i, params=payload)
        else:
            response = requests.request(url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        method=i, data=payload)
        print(j, "method for", i, " request: ", response.text)
