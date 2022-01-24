from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Flight, Ticket
from users.permissions import IsAdmin, IsPassenger
from .serializers import AdminFlightSerializer, PassengerFlightSerializer, PassengerTicketSerializer, \
    PassengerBookedTicketsSerializer
from rest_framework.generics import ListAPIView
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class AdminFlightsViewSet(ModelViewSet):
    queryset = Flight.objects.select_related('departure', 'destination').prefetch_related('ticket_ranks').all()
    permission_classes = [IsAdmin]
    serializer_class = AdminFlightSerializer


class AvailableFlightsView(ListAPIView):
    queryset = Flight.objects.select_related('departure', 'destination'). \
        prefetch_related('ticket_ranks__tickets').filter(booking_closed=False)
    permission_classes = [IsPassenger | IsAdmin, ]
    serializer_class = PassengerFlightSerializer


class PassengerTicketViewSet(ModelViewSet):
    permission_classes = [IsPassenger | IsAdmin, ]

    def get_queryset(self):
        if reverse('tickets') == self.request.path and self.request.method == 'GET':
            return Flight.objects.select_related('departure', 'destination'). \
                prefetch_related('ticket_ranks__tickets').filter(
                ticket_ranks__tickets__passenger=self.request.user).distinct()

        return Ticket.objects.select_related('ticket_rank').filter(passenger=self.request.user)

    def get_serializer_class(self):
        if reverse('tickets') == self.request.path and self.request.method == 'GET':
            return PassengerBookedTicketsSerializer

        return PassengerTicketSerializer

    def create(self, request, *args, **kwargs):
        request.data['passenger'] = request.user

        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.filter(pk=kwargs['pk']).exists():
            return Response(data={'message': _('The ticket is not found in passenger\'s booked tickets')},
                            status=status.HTTP_403_FORBIDDEN)

        return super().retrieve(request, *args, **kwargs)
