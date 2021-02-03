from django.urls import path, re_path
from . import views

app_name = "food_items"

urlpatterns = [
    path("product_details/<str:product_code>/",
         views.product_details, name="product_details"),
    path("favorite_details/<str:product_code>/",
         views.favorite_details, name="favorite_details"),
    re_path(r'^search_results/$',
            views.search_results,
            name="search_results"),
    path('favorites/', views.fetch_favorites, name="favorites"),
    path('record_product/<str:product_code>/',
         views.record_product,
         name="record_product"),

]
