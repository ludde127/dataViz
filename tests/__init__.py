

test_server = False
if not test_server:
    api_key = "3fa2846c-37fc-45f0-a87b-73bf567e23c0"
    names = ["a", "b", "c"]
    url = "http://127.0.0.1:8000/data/access/" + api_key
else:
    api_key = "6258e3c5-315d-42d4-a6fc-7cebf4abea98"
    names = ["a", "b", "c"]
    url = "https://llindholm.com/data/access/" + api_key

headers={'Authorization': 'TOK:<mAmq8-3c880bMCmxy_LQkUJyV_r4-uR09zvu0tLEDz4>'}