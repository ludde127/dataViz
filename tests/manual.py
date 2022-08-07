from pprint import pprint

import requests
from tests import url, names, headers
from tests.api import random_floats
resp = requests.put(url, json=random_floats(names, 100), headers=headers)
pprint(resp.text)