from food_items.models import Product, Store, BestProductSelection, Category
from django.contrib.auth.models import User


def set_up_db():
    Category.objects.bulk_create([
        Category(name="Snacks"),
        Category(name="Snacks sucrés"),
        Category(name="Petit-déjeuners"),
        Category(name="Biscuits"),
        Category(name="Biscuits et gâteaux"),
        Category(name="Snacks salés")])
    Store.objects.bulk_create([
        Store(name="Carrefour"),
        Store(name="Leclerc"),
        Store(name="Magasins U"),
        Store(name="REWE")])
    Product.objects.bulk_create([
        Product(name="Nutella Allégé",
                brand="Nutella Ferrero",
                code="01234567891011",
                last_modified="2020-11-11 15:45+0200",
                nutrition_score="E"
                ),
        Product(name="Nutella Délicieux",
                brand="Nutella Ferrero",
                code="32134567891011",
                last_modified="2020-11-11 19:45+0200",
                nutrition_score="C"
                ),
        Product(name="Goldbären",
                brand="Haribo",
                code="9999999999999",
                last_modified="2020-12-25 19:45+0200",
                nutrition_score="B")
    ])
    p1 = Product.objects.get(code="01234567891011")
    p2 = Product.objects.get(code="32134567891011")
    p3 = Product.objects.get(code="9999999999999")
    s1 = Store.objects.get(name="Carrefour")
    s2 = Store.objects.get(name="Leclerc")
    p1.stores.set([s1, s2])
    p2.stores.set([s2])
    p1.save()
    p2.save()

    User.objects.bulk_create([
        User(first_name="Fabrice",
             last_name="Jaouën",
             email="fabricejaouen@yahoo.com",
             is_superuser=True,
             username="admin",
             password="pwd",
             is_staff=True,
             is_active=True,
             date_joined="2020-11-01T05:48:00.941Z"),
        User(first_name="John",
             last_name="Doe",
             email="fabricejaouen@yahoo.com",
             is_superuser=False,
             username="user",
             password='pwd',
             is_staff=False,
             is_active=True,
             date_joined="2020-11-01T05:48:00.941Z"),
    ])

    u1 = User.objects.get(username="user")
    p1.selection.set([u1])
    p2.selection.set([u1])

    u2 = User.objects.get(username="admin")
    p3.selection.set([u2])
