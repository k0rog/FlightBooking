from django.db import models
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Flight(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    departure = models.ForeignKey(City, on_delete=models.CASCADE, related_name='outbound_flights', db_index=True)
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='incoming_flights')

    creation_date = models.DateField(default=timezone.now)

    booking_closed = models.BooleanField(default=False)


class TicketRank(models.Model):
    class Meta:
        unique_together = (('rank', 'flight'),)
    ECONOMY = 'EC'
    BUSINESS = 'BU'
    DELUXE = 'DE'

    TICKET_RANKS = (
        (ECONOMY, 'Economy'),
        (BUSINESS, 'Business'),
        (DELUXE, 'Deluxe'),
    )

    rank = models.CharField(max_length=2, choices=TICKET_RANKS)
    tickets_total = models.IntegerField()
    ticket_price = models.IntegerField()

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='ticket_ranks')


class Ticket(models.Model):
    passenger = models.ForeignKey('users.Passenger', on_delete=models.CASCADE, related_name='tickets')
    ticket_rank = models.ForeignKey(TicketRank, on_delete=models.CASCADE, related_name='tickets')
