"""
    This short module aims at filling the database for a first use.

    Classes:
        Command: please refer to Django official documentation for detailed.
        explanation.

    Exception:
        NIL

    Functions:
        NIL
"""

from django.core.management.base import BaseCommand
from food_items.openfoodfacts.off_data_process\
    import ProcessStore, ProcessCategory, ProcessProduct


class Command(BaseCommand, ProcessCategory, ProcessStore, ProcessProduct):
    help = "DB initialization for first use"

    def handle(self, *args, **options):
        stores = ProcessStore()
        stores.store_full_process()

        categories = ProcessCategory()
        categories.category_full_process()

        products = ProcessProduct()
        number_recorded_products = products.manage_full_set_products(self.NUMBER_OF_PAGES)
        products.product_upload_outcome(number_recorded_products)
