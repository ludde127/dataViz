

test_server = False
if not test_server:
    api_key = "fcc8a2f7-e073-4e30-bb37-326c4676418f"
    names = ["a", "b", "c"]
    url = "http://127.0.0.1:8000/data/access/" + api_key
else:
    api_key = "6258e3c5-315d-42d4-a6fc-7cebf4abea98"
    names = ["a", "b", "c"]
    url = "https://llindholm.com/data/access/" + api_key

headers={'Authorization': 'TOK:<-p1J6G-kGmlwO5u_fifBdE8qen8yBo2JVygN-zbavTk>'}