from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=560)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=280)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=14, unique=True)
    brand = models.CharField(max_length=400)
    name = models.CharField(max_length=400)
    last_modified = models.DateTimeField()
    nutrition_score = models.CharField(max_length=1)
    selection = models.ManyToManyField(User, through='BestProductSelection')
    stores = models.ManyToManyField(Store)
    categories = models.ManyToManyField(Category)
    image_url = models.URLField(null=True,
                                blank=True,
                                default="https://static.openfoodfacts.org/images/misc/openfoodfacts-logo-en-178x150.png")

    def __str__(self):
        return self.code


class BestProductSelection(models.Model):
    date_selection = models.DateTimeField(auto_now_add=True)
    code = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
