import json

json_txt = ('{"messages": [{"message": "This is the first message", "timestamp": "2021-06-04 16:40:53"},{"message": '
            '"And this is a second message", "timestamp": "2021-06-04 16:41:01"}]}')
obj = json.loads(json_txt)

print(obj["messages"][1]['message'])

# And this is a second message