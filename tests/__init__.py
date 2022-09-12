test_server = False
if not test_server:
    api_key = "1f69ec31-20fe-4722-9463-25d906fc9283"
    names = ["a", "b", "c"]
    url = "http://127.0.0.1:8000/data/access/" + api_key
else:
    api_key = "6258e3c5-315d-42d4-a6fc-7cebf4abea98"
    names = ["a", "b", "c"]
    url = "https://llindholm.com/data/access/" + api_key

headers={'Authorization': 'TOK:<vF_jH8zcKvKILmqj9wSEKajItY2F3PM_DTmfyGbvcEw>'}


