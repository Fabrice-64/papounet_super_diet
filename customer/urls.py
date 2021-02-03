from django.urls import path

from . import views

app_name = "customer"
urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('personal_infos/', views.personal_infos, name="personal_infos"),
    path('terms_of_use/', views.terms_of_use, name="terms_of_use"),
    path('contact/', views.contact, name="contact"),
]
