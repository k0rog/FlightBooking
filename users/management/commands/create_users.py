from django.core.management.base import BaseCommand
from users.models import Passenger, Admin


class Command(BaseCommand):
    def handle(self, *args, **options):
        passenger, _ = Passenger.objects.get_or_create(email='passenger@passenger.com')
        passenger.set_password('passenger')
        passenger.save()

        admin, _ = Admin.objects.get_or_create(email='admin@admin.com')
        admin.set_password('admin')
        admin.save()
