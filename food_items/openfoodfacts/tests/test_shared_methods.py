"""
    Data from Open Food Facts need to be cleaned up before being inserted
    into the DB. This module is testing this process.

    Please refer to the module shared_methods.py for a detailed explanation.
"""

from food_items.openfoodfacts.shared_methods import DataCleaning
from food_items.openfoodfacts.tests.mock_data import MockDataOFF
from django.test import TestCase


class TestDataCleaning(TestCase, DataCleaning, MockDataOFF):

    def test_check_special_characters(self):
        values = ["",
                  "le-magasin",
                  "l'autre magasin"]
        test_list = []
        for value in values:
            result = self._check_special_characters(value)
            test_list.append(result)
        self.assertIsNotNone(result)
        self.assertEqual(test_list, ["NaN", "le magasin", "l\'autre magasin"])

    def test_select_data(self):
        data = self.store_data
        key_file, key_to_check, threshold = "tags", "products", 1000
        selected_data = self._select_data(data, key_file,
                                          key_to_check, threshold)
        self.assertLess(len(selected_data), 100)

    def test_from_data_to_list(self):
        data = self.store_data
        key_file, key_item, key_to_check, threshold =\
            "tags", "name", "products", 1000
        store_list = self.from_data_to_list(data, key_file, key_item,
                                            key_to_check, threshold)
        self.assertGreater(len(store_list), 10)
        return store_list

    def test_assign_url(self):
        values = ["", "null", "https://test_url.com"]
        test_url = self.assign_url(values[0])
        self.assertEqual(test_url,
                         "https://static.openfoodfacts.org/images/misc/openfoodfacts-logo-en-178x150.png")
        test_url = self.assign_url(values[1])
        self.assertEqual(test_url,
                         "https://static.openfoodfacts.org/images/misc/openfoodfacts-logo-en-178x150.png")
        test_url = self.assign_url(values[2])
        self.assertEqual(test_url, "https://test_url.com")
