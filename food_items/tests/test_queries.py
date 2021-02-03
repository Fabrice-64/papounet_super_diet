"""
    This module contains the test queries user by a normal user of the website,
    in the management of his product search and recording.
    Each of them checks that the operation was duly processed with a mock DB.

    Classes:
        QueriesTest

    Exceptions:
        NIL
"""

from food_items import queries as q
from . import fixture as f
from django.test import TestCase
from food_items.models import Product, BestProductSelection
from django.contrib.auth.models import User


class QueriesTest(TestCase):
    def setUp(self):
        f.set_up_db()

    def test_query_search_results(self):
        result = q.query_search_results('Nutella')
        self.assertIsNotNone(result)

    def test_query_record_best_product(self):
        length = BestProductSelection.objects.count()
        product_to_record = Product.objects.get(code='01234567891011')
        user = User.objects.get(username='user')
        q.query_record_best_product(product_to_record, user)
        self.assertEqual(length + 1, BestProductSelection.objects.count())

    def test_query_get_favorites_code(self):
        user = User.objects.get(username='user')
        results = q.query_get_favorites_code(user)
        self.assertEqual(len(results), 2)
        self.assertLess(results[1].date_selection, results[0].date_selection)

    def test_fetch_favorites(self):
        user = User.objects.get(username='user')
        results = q.query_fetch_favorites(user)
        self.assertEqual(results[0].name, "Nutella Délicieux")

    def test_query_product_details(self):
        result = q.query_product_details('01234567891011')
        self.assertIsNotNone(result)
