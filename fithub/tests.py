import json

from django.test import TestCase, Client, tag
from .models import UserDetail
from django.contrib.auth.models import User


class ActionTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user("test1", "a@a.com", "1234")
        cls.user_id = user.pk
        detail = UserDetail(user=user, phone='09568749632', balance=0)
        detail.save()
        cls.client = Client()

    def test_signup(self):
        response = self.post_url('/sign_up', {'username': 'soodehb', 'password': '1234',
                                              'email': 'soodeh@gmail.com', 'phone': '09133333340', 'license_number': '466'})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.post_url(
            '/login', {'username': 'test1', 'password': '1234'})
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))
        self.assertNotEqual(content['user_id'], None)

        response = self.post_url(
            '/login', {'username': 'test1', 'password': 'false-password'})
        self.assertEqual(response.status_code, 400)

    def test_insert_history(self):
        response = self.post_url('/insert_history', {'user_id': self.user_id, 'history_type': 1,
                                                     'details': '', 'value': '12'})
        self.assertEqual(response.status_code, 200)

    def test_get_history(self):
        self.post_url('/insert_history', {'user_id': self.user_id, 'history_type': 1,
                                          'details': '', 'value': '12'})
        response = self.post_url('/get_history', {'user_id': self.user_id})
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))
        histories = content['histories']
        self.assertEqual(len(histories), 1)

    def post_url(self, url,  data):
        return self.client.post(url, json.dumps(data), content_type="application/json")
