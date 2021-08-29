from django.test import TestCase
from django.contrib.auth.models import User
from django.urls.base import resolve
from .views import cart, guide, products, home, search

# Create your tests here.


class URLTestsCase(TestCase):

    def test_testhomepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_procuts_page(self):
        found = resolve('/products/')
        self.assertEqual(found.func, products)

    def test_guide_page(self):
        found = resolve('/guide/')
        self.assertEqual(found.func, guide)

    def test_search_page(self):
        found = resolve('/search/')
        self.assertEqual(found.func, search)

    def test_guide_page(self):
        found = resolve('/cart/')
        self.assertEqual(found.func, cart)




class UserTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_user_exist(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

