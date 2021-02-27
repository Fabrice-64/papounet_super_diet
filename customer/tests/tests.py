from django.test import Client, TestCase
from django.contrib.auth.models import User
import customer.views as cv
from django.http import HttpResponse
from food_items.tests import fixture
from customer import functions
from django.contrib.auth.forms import ValidationError
from django.core import mail


class FunctionsTest(TestCase):
    def setUp(self):
        fixture.set_up_db()

    def test_check_password(self):
        # Test password compliance.
        test_password1 = "012345678"
        test_password2 = "012345678"
        try:
            functions.check_password(test_password1, test_password2)
        except ValidationError:
            self.assertRaises(ValidationError)


class SimpleTest(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_register(self):
        response = self.client.post('/customer/register/')
        self.assertTemplateUsed(response, 'customer/register.html')
        self.assertEqual(response.status_code, 200)

    def test_register_hardened_pwd(self):
        response = self.client.post('/customer/register/')
        self.assertTemplateUsed(response, 'customer/register.html')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get('/customer/')
        self.assertTemplateUsed(response, 'customer/home.html')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        user = User.objects.create_user(username='new_user', password="pwd")
        user.save()
        logged_in = self.client.login(username='new_user', password='pwd')
        self.assertTrue(logged_in)
        response = self.client.post('/customer/login/', {"username": 'new_user', 'password': 'pwd'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/home.html')

    def test_login_error(self):
        user = User.objects.create_user(username='new_user_error', password="pwd")
        user.save()
        response = self.client.post('/customer/login/', {'username': 'new_user_error', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/failed_login.html')
        self.assertTemplateNotUsed(response, 'customer/home.html')

    def test_user_logout(self):
        response = self.client.get('/customer/logout/')
        self.assertTemplateUsed(response, 'customer/home.html')
        self.assertEqual(response.status_code, 200)


class ChangePasswordTest(TestCase):

    def SetUp(self):
        self.client = Client()

    def test_password_change(self):
        test_user2 = User.objects.create_user(username="test_user2", password='user2')
        test_user2.save()
        self.client.post('/customer/login/', {'username': 'test_user2', 'password': 'user2'})
        response = self.client.post('/customer/password_change/', {'username': 'test_user2',
                                    'current_password': 'user2', 'new_password': 'user3',
                                                                   'new_password2': 'user3'})
        self.assertTemplateUsed(response, 'customer/password_change.html')


class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Subject here', 'password_change',
            'contact@papounet-super-diet.fr', ['to@example.com'],
            fail_silently=False,
        )
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
