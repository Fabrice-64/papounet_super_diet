from django.test import Client, TestCase


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
