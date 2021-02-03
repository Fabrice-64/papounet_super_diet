"""
    Manage database changes, like upload and delete.
    It is specifically designed with Django ORM syntax.

    Classes:
        UploadQueries

        DeleteQueries

    Exceptions:
        NIL

    Functions:
        NIL
"""

from food_items.models import Product, Store, Category
from datetime import datetime, timezone


class UploadQueries():
    def query_upload_stores(self, store_list):
        store_list = [Store(name=store) for store in store_list]
        Store.objects.bulk_create(store_list)

    def query_upload_categories(self, category_list):
        category_list = [Category(name=category) for category in category_list]
        Category.objects.bulk_create(category_list)

    def _list_products_for_db(self, product_list):
        product_objects = [(Product(
            code=item[2],
            brand=item[0],
            name=item[1],
            last_modified=datetime.fromtimestamp(
                int(item[7]), timezone.utc),
            nutrition_score=item[3],
            image_url=item[6])) for item in product_list]
        return product_objects

    def _add_products_to_db(self, product_list):
        products_for_upload = self._list_products_for_db(product_list)
        Product.objects.bulk_create(products_for_upload)

    def _add_stores_categories_to_product(self, product_list):
        """
            As stores and categories are linked to products through
            join tables, their relation is established here.

            Arguments:
                product_list: to be noticed, Stores and Categories
                have already been converted into a list.

            Returns:
                None.
        """
        for item in product_list:
            # As we check if categories and stores exist, we avoid exceptions.
            existing_stores = [store.name for store in Store.objects.all()]
            existing_categories = [category.name
                                   for category in Category.objects.all()]
            product = Product.objects.get(code=item[2])
            store_list = [Store.objects.get(name=store)
                          for store in item[4] if store in existing_stores]
            category_list = [Category.objects.get(name=category)
                             for category in item[5]
                             if category in existing_categories]
            product.stores.set(store_list)
            product.categories.set(category_list)
            product.save()

    def query_upload_products(self, product_list):
        self._add_products_to_db(product_list)
        self._add_stores_categories_to_product(product_list)

    def query_count_products(self):
        return Product.objects.count()


class DeleteQueries:

    def query_delete_all_categories(self):
        Category.objects.all().delete()

    def query_delete_all_stores(self):
        Store.objects.all().delete()

    def query_delete_all_products(self):
        Product.objects.all().delete()


class UpdateQueries:

    def query_fetch_all_stored_products(self):
        return {product.code: (product.last_modified, product.stores.all()) for product in Product.objects.all()}

    def query_fetch_existing_stores(self):
        return [store.name for store in Store.objects.all()]

    def query_update_product(self, product, existing_stores):
        Product.objects.filter(code=product[2]).update(
            brand=product[0],
            name=product[1],
            nutrition_score=product[3],
            image_url=product[6],
            last_modified=datetime.fromtimestamp(
                int(product[7]), timezone.utc)
        )
        store_list = [Store.objects.get(name=store)
                      for store in product[4] if store in existing_stores]
        product_in_db = Product.objects.get(code=product[2])
        product_in_db.stores.set(store_list)
        product_in_db.save()
