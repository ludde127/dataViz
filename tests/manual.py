from pprint import pprint

import requests

api_key = "3fa2846c-37fc-45f0-a87b-73bf567e23c0"
names = ["a", "b", "c"]

url = "http://127.0.0.1:8000/data/access/" + api_key

resp = requests.post(url, json={"a": 2, "b": 3, "c": 4})
pprint(resp)