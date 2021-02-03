"""
    This short module empties the products, stores and categories
    from the database.
    It doesn't affect the users' accounts.

    Classes:
        Command: please refer to Django official documentation for detailed.
        explanation.

    Exceptions:
        NIL

    Functions:
        NIL
"""
from django.core.management.base import BaseCommand
from food_items.openfoodfacts.off_data_process\
    import UpdateProducts
from food_items.openfoodfacts.config import OpenFoodFactsParams


class Command(BaseCommand, UpdateProducts, OpenFoodFactsParams):
    help = "Update the products"

    def handle(self, *args, **options):
        product_count, update_counter = self.update_products_in_db(self.NUMBER_OF_PAGES)
        self.print_update_outcome(product_count, update_counter)
