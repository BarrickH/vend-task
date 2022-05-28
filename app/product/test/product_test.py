import unittest

import requests


class ProductApiTest(unittest.TestCase):
    tenant_id = "vend_barrick"
    API_URL = "http://127.0.0.1:8090"
    product_URL = "{}/{}/api/1.0/products".format(API_URL,tenant_id)
    product_dict = {
        "name": "test_product",
        "price": "1"
    }
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyZWYiOiIzNDRiZWQyZi00YzRkLTQxOGYtOWQ0MC1jODYwNGZkNWM0ODQiLCJhdWQiOiI5ZjUyLTl6YzMtNGUxMS05YzU4LTR4MDciLCJpc3MiOiJWRU5EX1RBU0tfREVNT19GTEFTSyIsImV4cCI6MTY1Mzc4MTE4Nn0.BwgkbnRxlujLn0PHAPF6w4F-Jhw9TNieyuGrbs_4UhTTIXRwwcss8YgPBd1wnIt9zviDFICIxapcDYq37m6Feg',
        'Content-Type': 'application/json'
    }

    # test list all product endpoint
    def test_1_get_all_product(self):
        r = requests.get(self.product_URL,headers=self.headers)
        self.assertEqual(r.status_code,200)
        self.assertTrue(len(r.json()))

    # test create product endpoint
    def test_2_create_new_product(self):
        r = requests.post(self.product_URL, json=self.product_dict, headers=self.headers)
        self.assertEqual(r.status_code,200)

    # test the new product can be obtain
    def test_3_get_new_product(self):
        r = requests.get(self.product_URL, headers=self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[-1].get('name'),'test_product')
        self.assertDictEqual(r.json()[-1],self.product_dict)