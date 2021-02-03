
import os


class OpenFoodFactsParams:

    URL = 'https://fr.openfoodfacts.org/cgi/search.pl?'

    HEADERS = {'User-Agent': 'python-requests/2.22.0'}

    URL_STATIC = 'https://fr.openfoodfacts.org/'

    URL_STORES = os.path.join(URL_STATIC, 'stores.json')

    URL_CATEGORIES = os.path.join(URL_STATIC, 'categories.json')

    payload = {
        'tagtype_0': 'categories', 'tag_contains_0': 'contains',
        'tag_0': '', 'tag_types_1': 'countries',
        'tag_contains_1': 'contains', 'tag_1': 'fr',
        'json': 1, 'action': "process",
        "page_size": 1000, 'page': ""}

    URL_SEARCH = 'cgi/search.pl?search_simple=1'

    URL_PRODUCTS = os.path.join(URL_STATIC, URL_SEARCH)

    CATEGORY = "Snacks"

    NUMBER_OF_PAGES = 3
