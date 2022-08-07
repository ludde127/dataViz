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


class Data(unittest.TestCase):
    names = ("a", "b", "c")

    def setUp(self) -> None:
        requests.delete(url, headers=headers)

    def one_random_request(self):
        d = random_dict(self.names)
        resp = requests.post(url, json=d, headers=headers)
        self.assertTrue(resp.status_code == 200, "response errored for json " + str(d))
        return d

    def test_post_one_by_one(self):
        for _ in range(100):
            self.one_random_request()

    def test_get_status_code(self):
        self.assertTrue(requests.get(url, headers=headers).status_code==200, "Get did not work for url " + url)

    def test_verify_post_change(self):
        old = requests.get(url, headers=headers)
        change = self.one_random_request()
        as_csv_row = ",".join([str(change[c]) for c in ("a", "b", "c")])
        new = requests.get(url, headers=headers)
        self.assertEqual(as_csv_row, str(new.text).split("\n")[-1])
        self.assertNotEqual(old.text, new.text)
        self.assertTrue(len(old.text) < len(new.text))

    def test_delete(self):
        requests.delete(url, headers=headers)
        self.assertEqual("", requests.get(url, headers=headers).text)

    def test_put(self):
        self.one_random_request()
        self.one_random_request()
        self.one_random_request()

        requests.put(url, random_dict(self.names), headers=headers)
        self.assertEqual(1, len(requests.get(url, headers=headers).text.split("\n")))


if __name__ == "__main__":
    unittest.main()