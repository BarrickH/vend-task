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

    # test list all product endpoint
    def test_1_get_all_product(self):
        r = requests.get(self.product_URL)
        self.assertEqual(r.status_code,200)
        self.assertTrue(len(r.json()))

    # test create product endpoint
    def test_2_create_new_product(self):
        r = requests.post(self.product_URL, json=self.product_dict)
        self.assertEqual(r.status_code,201)

    # test the new product can be obtain
    def test_3_get_new_product(self):
        r = requests.get(self.product_URL)
        self.assertEqual(r.json()[-1].get('name'),'test_product')