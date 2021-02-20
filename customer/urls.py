from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    # Change password !
    path('password_change/', views.password_change, name="password_change"),
    path('password_change_done/', views.password_change_done, name="password_change_done"),
    # Reset password !
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(
        template_name="customer/password_reset_form.html",
        email_template_name="customer/password_reset_e-mail.html",
        success_url="done/"), 
        name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
        template_name="customer/password_reset_done.html"
        ), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
        template_name="customer/password_reset_confirm.html",
        success_url="reset/done/",
        post_reset_login=True
        ),
        name='password_reset_confirm'),
    path('reset/Mjg/set-password/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="customer/password_reset_complete.html"
    ), name='password_reset_complete')
]
