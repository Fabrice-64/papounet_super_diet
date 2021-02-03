"""
    This module tests the step-by-step processing of the data from the download
    from Open Food Facts to the upload in the database.
    Tests are arranged in accordance with the type of data:
    Stores, Categories, Products.

    Classes:
        TestConnectionOFF: tests the effective connection with Open Food Facts:
        we should get a 200 OK response type. No data is downloaded.

        TestProcessStore: organized in two steps : effective data download and
        processing of a mock dataset for test purposes.

        TestProcessCategory: built on the same principles than the stores

        TestUploadProduct: checks that a product is correctly processed to
        be added to the DB, including its relation to the join tables.

        TestProcessProduct: test the full process of a product:
        - construction of the download request,
        - data processing,
        - upload in a test DB.

    Exceptions:
        NIL

    Functions:
        NIL
"""

import requests
import json
from django.test import TestCase
from food_items.tests import fixture as f
from food_items.models import Product, Store, Category
from food_items.openfoodfacts.off_data_process \
    import ProcessStore, ProcessCategory, ProcessProduct, UpdateProducts
from food_items.openfoodfacts.config import OpenFoodFactsParams
from food_items.openfoodfacts.tests.mock_data import MockDataOFF, MockProducts
from food_items.openfoodfacts.queries import DeleteQueries, UploadQueries, UpdateQueries
from unittest.mock import Mock, patch
from datetime import datetime, timezone


class TestConnectionOFF(TestCase, OpenFoodFactsParams):
    def test_connexion_OFF(self):
        r = requests.get(self.URL, headers=self.HEADERS)
        self.assertEqual(r.status_code, 200)


class TestProcessStore(TestCase, ProcessStore, OpenFoodFactsParams,
                       MockDataOFF):
   
    @patch('requests.get')
    def test_store_full_process(self, mock_get):
        self.stores = self.from_data_to_list(self.store_data, "tags",
                                             "name", "products", 1000)
        self._upload_stores(self.stores)
        self.assertGreater(Store.objects.count(), 20)
        self.assertLess(Store.objects.count(), 100)


class TestProcessCategory(TestCase, ProcessCategory, OpenFoodFactsParams,
                          MockDataOFF):
    
    @patch('requests.get', autospec=True)
    def test_category_full_process(self, mock_get):
        self.categories = self.from_data_to_list(self.category_data,
                                                 "tags", "name", "products",
                                                 10000)
        self._upload_categories(self.categories)
        self.assertGreater(Category.objects.count(), 20)
        self.assertLess(Category.objects.count(), 200)


class TestUploadProduct(TestCase, MockProducts, MockDataOFF, ProcessProduct, DeleteQueries):
    def setUp(self):
        f.set_up_db()

    def test_query_upload_products(self):
        try:
            Product.objects.get(name="P'tit Nature Complet Test")
            self.fail("Le Produit est déjà en base !!")
        except Exception:
            self.query_upload_products(self.mock_product_list)
            product = Product.objects.get(name="P'tit Nature Complet Test")
            self.assertIsNotNone(product)
            self.assertEqual(len(
                [store.name for store in product.stores.all()]), 1)
            self.assertEqual(len(
                [category.name for category in product.categories.all()]), 1)

    @patch("requests.get")
    def test_manage_full_set_products(self, mock_get):
        self.query_delete_all_products()
        mock_get.return_value.json.return_value = self.product_data
        self.manage_full_set_products(1)
        result = self.query_count_products()
        self.assertEqual(result, 20)


class TestProcessProduct(TestCase, ProcessProduct, OpenFoodFactsParams,
                         MockDataOFF):
    def setUp(self):
        f.set_up_db()

    def test_configure_request_payload(self):
        test_page_number = 1
        self.request_payload = self._configure_request_payload(
            test_page_number)
        self.assertEqual(self.test_payload, self.request_payload)

    def test_sort_out_product_data(self):
        data_to_sort_out = self.product_data
        self.data_sorted_out = self._sort_out_product_data(data_to_sort_out)
        self.assertEqual(len(self.data_sorted_out), 20)

    @patch("requests.get")
    def test_product_treatment(self, mock_get):
        mock_get.return_value.json.return_value = self.updated_products_data
        product_list = self._product_treatment()
        self.assertEqual(len(product_list), 3)
        self.assertEqual(len(product_list[0]), 8)


class TestUpdateProduct(TestCase, UpdateProducts, MockDataOFF):
    def setUp(self):
        f.set_up_db()

    def __download_updated_products(self):
        self.mock_response = Mock(return_value=self.updated_products_data)
        return self.mock_response.return_value

    def test_fetch_all_stored_products(self):
        self.stored_products = self.query_fetch_all_stored_products()
        self.assertEqual(len(self.stored_products), 3)

    def test_store_comparrison(self):
        product_to_update_stores = ["Leclerc", "Auchan"]
        current_stores = ["Carrefour"]
        result = self._store_comparrison(product_to_update_stores, current_stores)
        self.assertEqual(result, product_to_update_stores)

    @patch("requests.get")
    def test_product_comparrison(self, mock_get):
        mock_get.return_value.json.return_value = self.updated_products_data
        self.stored_products = self.query_fetch_all_stored_products()
        products_for_update = self._product_treatment()
        result_update, result_create = self._product_comparrison(self.stored_products, products_for_update)
        self.assertEqual(len(result_update), 2)
        self.assertEqual(result_update[0][4], ["Carrefour", "REWE"])
        self.assertEqual(len(result_create), 1)

    @patch('requests.get')
    def test_compare_products(self, mock_get):
        mock_get.return_value.json.return_value = self.updated_products_data
        stored_products = self.query_fetch_all_stored_products()
        products_to_update, products_to_create = self._compare_products(stored_products, 1)
        self.assertEqual(len(products_to_update), 2)
        self.assertEqual(products_to_update[0][4], ["Carrefour", "REWE"])
        self.assertEqual(len(products_to_create), 1)
        self.assertEqual(products_to_create[0][1], "Goldbären Nouveau Produit")

    @patch('requests.get')
    def test_update_products_in_db(self, mock_get):
        mock_get.return_value.json.return_value = self.updated_products_data
        self.update_products_in_db(2)
        result_update = self.query_fetch_all_stored_products()
        self.assertEqual(len(result_update), 4)
