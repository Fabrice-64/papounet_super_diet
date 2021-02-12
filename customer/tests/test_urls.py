from django.test import Client, TestCase
from django.contrib.auth.models import User


class SimpleTest(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_register(self):
        response = self.client.get('/customer/register/')
        self.assertTemplateUsed(response, 'customer/register.html')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get('/customer/')
        self.assertTemplateUsed(response, 'customer/home.html')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        self.client.login(username='user', password='pwd')
        response = self.client.get('/customer/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/login.html')

    def test_user_logout(self):
        response = self.client.get('/customer/logout/')
        self.assertTemplateUsed(response, 'customer/home.html')
        self.assertEqual(response.status_code, 200)


class ChangePasswordTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user2 = User.objects.create_user(username="user2", password='user2')
        test_user3 = User.objects.create_user(username="user3", password="user3")
        test_user2.save()
        test_user3.save()

    def test_user_change_password(self):
        response = self.client.post('/customer/password_change/')
        self.assertTemplateUsed(response, 'customer/password_change.html')
        # self.assertEquals(response.satus_code, 200)
