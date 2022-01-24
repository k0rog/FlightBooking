import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from flights.serializers import PassengerFlightSerializer, AdminFlightSerializer
from users.tests import TestAuthenticateAdminMixin, TestAuthenticatePassengerMixin
from flights.models import City, Flight

FLIGHT_CREATION_DATA = {
    'start_datetime': '2022-01-18T18:30+00:00',
    'end_datetime': '2022-01-18T21:40+03:00',
    'departure': 1,
    'destination': 2,
    'ticket_ranks': [{
        'rank': 'EC',
        'tickets_total': 200,
        'ticket_price': 400
    },
        {
            'rank': 'DE',
            'tickets_total': 200,
            'ticket_price': 400
        }]
}


class AdminFlightsViewSetTestCase(TestAuthenticateAdminMixin, APITestCase):
    url_name = 'flights'
    url = reverse(url_name)

    def setUp(self):
        super().setUp()
        City.objects.bulk_create([
            City(name='Gomel'),
            City(name='London'),
            City(name='Berlin'),
        ])

    response_data = {
        'id': 1,
        'start_datetime': '2022-01-18T18:30:00Z',
        'end_datetime': '2022-01-18T18:40:00Z',
        'destination': {
            'id': 2,
            'name': 'London'
        },
        'departure': {
            'id': 1,
            'name': 'Gomel'
        },
        'ticket_ranks': [
            {
                'id': 1,
                'rank': 'EC',
                'ticket_price': 400,
                'tickets_total': 200
            },
            {
                'id': 2,
                'rank': 'DE',
                'ticket_price': 400,
                'tickets_total': 200
            }
        ],
        'booking_closed': False
    }

    def test_flight_creation(self):
        response = self.client.post(self.url, data=FLIGHT_CREATION_DATA, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), self.response_data)

    def test_flights_list(self):
        flight_1 = json.loads(self.client.post(self.url, data=FLIGHT_CREATION_DATA, format='json').content)
        flight_2 = json.loads(self.client.post(self.url, data=FLIGHT_CREATION_DATA, format='json').content)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json.loads(response.content), [flight_1, flight_2])


class AdminFlightsViewSetExactTestCase(TestAuthenticateAdminMixin, APITestCase):
    url_name = 'flights_admin_exact'
    url = reverse(url_name, kwargs={'pk': 1})

    def setUp(self):
        super().setUp()
        City.objects.bulk_create([
            City(name='Gomel'),
            City(name='London'),
            City(name='Berlin'),
        ])

        self.flight = json.loads(self.client.post(reverse('flights'), FLIGHT_CREATION_DATA, format='json').content)

    def test_retrieve_flight(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.flight)

    def test_update_destination_flight(self):
        self.flight['destination'] = {
            'id': 3,
            'name': 'Berlin'
        }

        response = self.client.patch(self.url, {'destination': 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.flight)

    def test_delete_flight(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content.decode(), '')


class AvailableFlightsViewTestCase(TestAuthenticatePassengerMixin, APITestCase):
    url_name = 'available_flights'
    url = reverse(url_name)

    def setUp(self):
        super().setUp()

        City.objects.bulk_create([
            City(name='Gomel'),
            City(name='London'),
            City(name='Berlin'),
        ])

        serializer = AdminFlightSerializer(data=FLIGHT_CREATION_DATA)

        if serializer.is_valid():
            serializer.save()
            json.loads(json.dumps(serializer.data))

        closed_flight = FLIGHT_CREATION_DATA.copy()
        closed_flight['booking_closed'] = True
        serializer = AdminFlightSerializer(data=closed_flight)
        if serializer.is_valid():
            serializer.save()

    def test_available_flight(self):
        response = self.client.get(self.url)

        available_flight = Flight.objects.filter(booking_closed=False).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [PassengerFlightSerializer(instance=available_flight).data])


class AvailableFlightsViewTestCaseAdmin(AvailableFlightsViewTestCase, TestAuthenticateAdminMixin):
    pass


class PassengerTicketViewSetTestCase(TestAuthenticatePassengerMixin, APITestCase):
    url_name = 'tickets'
    url = reverse(url_name)

    def setUp(self):
        super().setUp()

        City.objects.bulk_create([
            City(name='Gomel'),
            City(name='London'),
            City(name='Berlin'),
        ])

        serializer = AdminFlightSerializer(data=FLIGHT_CREATION_DATA)

        if serializer.is_valid():
            serializer.save()

    def test_booking(self):
        response = self.client.post(self.url, {'ticket_rank': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content),
                         {
                             'passenger': 1,
                             'ticket_rank': {
                                 'id': 1,
                                 'rank': 'EC',
                                 'ticket_price': 400,
                                 'tickets_left': 199
                             }
                         })

    def test_tickets_with_summary_per_flight(self):
        self.client.post(self.url, {'ticket_rank': 1}, format='json')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         [
                             {
                                 'id': 1,
                                 'start_datetime': '2022-01-18T18:30:00Z',
                                 'end_datetime': '2022-01-18T18:40:00Z',
                                 'departure': {
                                     'id': 1,
                                     'name': 'Gomel'
                                 },
                                 'destination': {
                                     'id': 2,
                                     'name': 'London'
                                 },
                                 'ticket_ranks': [
                                     {
                                         'id': 1,
                                         'rank': 'EC',
                                         'ticket_price': 400,
                                         'ticket_count': 1
                                     },
                                     {
                                         'id': 2,
                                         'rank': 'DE',
                                         'ticket_price': 400,
                                         'ticket_count': 0
                                     }
                                 ]
                             }
                         ]
                         )

    def test_retrieve_ticket(self):
        self.client.post(self.url, {'ticket_rank': 1}, format='json')

        response = self.client.get(reverse('ticket_exact', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {
                             'passenger': 1,
                             'ticket_rank': {
                                 'id': 1,
                                 'rank': 'EC',
                                 'ticket_price': 400,
                                 'tickets_left': 199
                             }
                         })

    def test_destroy_ticket(self):
        self.client.post(self.url, {'ticket_rank': 1}, format='json')

        response = self.client.delete(reverse('ticket_exact', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content.decode(), '')


