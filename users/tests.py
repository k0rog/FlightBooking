import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Group
from users.mixins import TestAuthenticatePassengerMixin, TestAuthenticateAdminMixin


class UserRegisterViewTestCase(APITestCase):
    def setUp(self):
        passenger_group, _ = Group.objects.get_or_create(name='passenger')
        admin_group, _ = Group.objects.get_or_create(name='admin')

    def test_registration(self):
        data = {
            'first_name': "Ilya",
            'last_name': 'Auramenka',
            'email': 'c@c.com',
            'password': 'c'
        }
        response = self.client.post(reverse('registration'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {'id': 1,
                                                        'first_name': 'Ilya',
                                                        'last_name': 'Auramenka',
                                                        'email': 'c@c.com',
                                                        })


class PassengerUserViewSetTestCase(TestAuthenticatePassengerMixin, APITestCase):
    url_name = 'user_exact'
    url = reverse(url_name, kwargs={'pk': 1})

    def test_user_update(self):
        response = self.client.patch(self.url, {'first_name': 'Peter'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'id': 1, 'first_name': 'Peter', 'last_name': 'Auramenka'})

    def test_user_delete(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content.decode(), '')

    def test_user_retrieve(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'id': 1, 'first_name': 'Ilya', 'last_name': 'Auramenka'})

    # permissions are work for all cases as we are testing one ViewSet so there is no need to write 3 different cases
    def test_other_user_retrieve(self):
        response = self.client.get(reverse(self.url_name, kwargs={'pk': 2}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail': 'You do not have permission to perform this action.'})


class AdminUserViewSetTestCase(TestAuthenticateAdminMixin, PassengerUserViewSetTestCase):
    def test_other_user_retrieve(self):
        response = self.client.get(reverse(self.url_name, kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {'detail': 'Not found.'})
