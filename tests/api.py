import random
import unittest
from pprint import pprint

import requests
from . import url, headers
import string
import numpy as np


def random_dict(names=("a", "b", "c")):
    x = np.random.randint(3, size=(1,))
    dictionary = dict()
    if x == 2:
        for name in names:
            # STRINGS
            dictionary[name] = "".join(random.choices(string.ascii_letters, k=25))
    elif x == 1:
        for name in names:
            # INTEGERS
            dictionary[name] = random.choices(range(1, 10000))[0]
    elif x == 0:
        for name in names:
            # FLOATS
            dictionary[name] = random.choices(range(1, 10000))[0]/3.3
    return dictionary


def random_floats(names, amount=1):
    dictionary = dict()
    for name in names:
        # FLOATS
        if amount == 1:
            dictionary[name] = random.choices(range(1, 10000))[0]/3.3
        else:
            c = list()
            for _ in range(amount):
                c.append(random.choices(range(1, 10000))[0]/3.3)
            dictionary[name] = c
    return dictionary

class HelperAPI:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get(self):
        return requests.get(self.url, headers=self.headers)

    def post(self, data: dict):
        return requests.post(self.url, data=data, headers=self.headers)

    def put(self, data: dict):
        return requests.put(self.url, data=data, headers=self.headers)

    def delete(self):
        return requests.delete(self.url, headers=headers)

    def nbr_of_rows(self):
        return len(requests.get(url, headers=headers).text.split("\n"))

helper = HelperAPI(url, headers)

class Data(unittest.TestCase):
    names = ("a", "b", "c")

    def setUp(self) -> None:
        helper.delete()

    def one_random_request(self):
        d = random_dict(self.names)
        resp = helper.post(d)
        self.assertTrue(resp.status_code == 200, "response errored for json " + str(d))
        return d

    def test_post_one_by_one(self):
        for _ in range(100):
            self.one_random_request()

    def test_get_status_code(self):
        self.assertTrue(helper.get().status_code==200, "Get did not work for url " + url)

    def test_verify_post_change(self):
        old = helper.get()
        change = self.one_random_request()
        as_csv_row = ",".join([str(change[c]) for c in ("a", "b", "c")])
        new = helper.get()
        self.assertEqual(as_csv_row, str(new.text).split("\n")[-1])
        self.assertNotEqual(old.text, new.text)
        self.assertTrue(len(old.text) < len(new.text))

    def test_delete(self):
        helper.delete()
        self.assertEqual("", helper.get().text)

    def test_put(self):
        self.one_random_request()
        self.one_random_request()
        self.one_random_request()
        helper.put(random_dict(self.names))
        self.assertEqual(1, helper.nbr_of_rows())


class MoreDataTest(unittest.TestCase):
    names = ("a", "b", "c")

    def setUp(self) -> None:
        helper.delete()

    def test_add_time_multiple(self):
        helper.delete()
        helper.post({"a": ["2020-12-01", "2020-12-09", "2021-02-09"], "b": [10, 3, 19], "c": [14, 12, 18]})
        print(helper.get().text)

        self.assertEqual(3, helper.nbr_of_rows())

    def test_add_time_one(self):
        helper.delete()
        helper.post({"a": "2020-12-01", "b": 10, "c": 14})

        self.assertEqual(1, helper.nbr_of_rows())

if __name__ == "__main__":
    unittest.main()