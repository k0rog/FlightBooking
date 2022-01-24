from django.core.management.base import BaseCommand
from flights.models import Flight
from datetime import datetime, timezone, timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        compare_datetime = datetime.now(timezone.utc)
        compare_datetime += timedelta(hours=2)
        Flight.objects.filter(start_datetime__lte=compare_datetime).update(booking_closed=True)
