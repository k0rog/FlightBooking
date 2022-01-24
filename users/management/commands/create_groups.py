from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
# from django.contrib.auth.models import Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        passenger_group, _ = Group.objects.get_or_create(name='passenger')
        admin_group, _ = Group.objects.get_or_create(name='admin')
