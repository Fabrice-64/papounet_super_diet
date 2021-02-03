from .models import Product, BestProductSelection
from django.contrib.auth.models import User


def query_search_results(searched_item):
    results = Product.objects.filter(
        name__icontains=searched_item).order_by("nutrition_score")[:6]
    return results


def query_record_best_product(product_to_record, user):
    product_to_record = Product.objects.get(code=product_to_record)
    user = User.objects.get(username=user)
    new_favorite = BestProductSelection(code=product_to_record, user=user)
    new_favorite.save()


def query_get_favorites_code(user):
    favorites = BestProductSelection.objects.filter(
        user=user).order_by('-date_selection')[:6]
    return favorites


def query_fetch_favorites(user):
    favorites_list = query_get_favorites_code(user)
    favorites = [Product.objects.get(
        code=favorite.code) for favorite in favorites_list]
    return favorites


def query_product_details(product_code):
    product_details = Product.objects.get(code=product_code)
    stores = ", ".join([store.name for store in product_details.stores.all()])
    return product_details, stores
