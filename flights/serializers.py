from rest_framework import serializers
from .models import Flight, TicketRank, Ticket, City
from datetime import datetime
from django.utils.translation import gettext_lazy as _


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class TicketRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketRank
        fields = ['id', 'rank', 'ticket_price']


class FlightSerializer(serializers.ModelSerializer):
    ticket_ranks = TicketRankSerializer(many=True)

    class Meta:
        model = Flight
        fields = ['id', 'start_datetime', 'end_datetime', 'departure', 'destination', 'ticket_ranks']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['destination'] = CitySerializer(instance=instance.destination).data
        representation['departure'] = CitySerializer(instance=instance.departure).data

        return representation

    def create(self, validated_data):
        ranks_data = validated_data.pop('ticket_ranks')
        flight = Flight.objects.create(**validated_data)

        TicketRank.objects.bulk_create([TicketRank(flight=flight, **rank_data) for rank_data in ranks_data])

        return flight

    def validate_end_datetime(self, value):
        start_datetime = self.initial_data.get('start_datetime',
                                               self.instance.start_datetime if self.instance else None)

        if not start_datetime:
            return None

        start_datetime = datetime.fromisoformat(start_datetime) \
            if not isinstance(start_datetime, datetime) else start_datetime

        if start_datetime >= value:
            raise serializers.ValidationError(_('Boarding time must be later than departure time'))

        return value

    def validate_destination(self, value):
        departure = self.initial_data.get('departure',
                                          self.instance.departure_id if self.instance else None)

        if not departure:
            return None

        if departure == value.id:
            raise serializers.ValidationError(_('Departure and destination cities must be not the same'))

        return value

    def validate_ticket_ranks(self, value):
        if len(value) > len(set([ticket_rank['rank'] for ticket_rank in value])):
            raise serializers.ValidationError(_('Ranks must be unique'))

        return value


class AdminTicketRankSerializer(TicketRankSerializer):
    class Meta:
        model = TicketRank
        fields = ['id', 'rank', 'ticket_price', 'tickets_total']


class AdminFlightSerializer(FlightSerializer):
    ticket_ranks = AdminTicketRankSerializer(many=True)

    class Meta:
        model = Flight
        fields = ['id', 'start_datetime', 'end_datetime', 'destination', 'departure', 'ticket_ranks', 'booking_closed']


class PassengerTicketRankSerializer(TicketRankSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tickets_left = instance.tickets_total - instance.tickets.count()
        representation['tickets_left'] = tickets_left
        return representation


class PassengerFlightSerializer(FlightSerializer):
    ticket_ranks = PassengerTicketRankSerializer(many=True)


class PassengerTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['passenger', 'ticket_rank']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ticket_rank = PassengerTicketRankSerializer(instance=instance.ticket_rank)
        representation['ticket_rank'] = ticket_rank.data
        return representation

    def validate(self, attrs):
        ticket_rank = attrs.get('ticket_rank')

        if ticket_rank.flight.booking_closed:
            raise serializers.ValidationError(_('Booking is already closed for this flight!'))

        return attrs


class TicketRankSummarySerializer(TicketRankSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ticket_count'] = instance.tickets.count()
        return representation


class PassengerBookedTicketsSerializer(FlightSerializer):
    ticket_ranks = TicketRankSummarySerializer(many=True)
