from os import name, path
from django.http import response
from django.shortcuts import redirect
from django.test import TestCase, RequestFactory
from .views import cart, home
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from .models import Cart, CartItem, Category, Headphones
from .views import cart

# Create your tests here.


class URLTests(TestCase):
    def test_testhomepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class ShopTestCase(TestCase):
    def setUp(self):
        self.user = User(username="noname", email="noname@example.com", password="dasd213sd@")
        self.user.save()

    def test_user_exist(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)




    # def test_login_url(self):
    #     # login_url = "/login"
    #     # self.assertEqual(settings.LOGIN_URL, login_url)
    #     login_url = settings.LOGIN_URL
    #     # response = self.client.post(url, {}, follow=True)
    #     data = {"username": "noname", "password": "dasd213sd@"}
    #     response = self.client.post(login_url, data, follow=True)
    #     print(response.request)
    #     # print(dir(response))
    #     status_code = response.status_code
    #     redirect_path = response.request.get("PATH_INFO")
    #     self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
    #     self.assertEqual(status_code, 200)