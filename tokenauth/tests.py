import json
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.utils import create_passenger, PASSENGER_DATA
from users.mixins import TestAuthenticatePassengerMixin
from users.models import Passenger


class LoginViewTestCase(APITestCase):
    url_name = 'login'
    url = reverse(url_name)

    def setUp(self) -> None:
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='passenger')

    def test_login(self):
        admin_group, _ = Group.objects.get_or_create(name='admin')

        user = create_passenger()

        response = self.client.post(self.url, {'email': user.email, 'password': PASSENGER_DATA['password']})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.cookies)
        self.assertEqual(response.cookies.get('token').value, user.auth_token.key)
        self.assertEqual(json.loads(response.content), {'user_id': 1, 'email': user.email})


class LogoutViewTestCase(TestAuthenticatePassengerMixin, APITestCase):
    url_name = 'logout'
    url = reverse(url_name)

    def test_logout(self):
        response = self.client.post(self.url)

        self.user = Passenger.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.cookies)
        self.assertFalse(hasattr(self.user, 'auth_token'))
        self.assertEqual(json.loads(response.content), {'message': 'success'})
