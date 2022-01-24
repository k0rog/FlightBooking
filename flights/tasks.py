from celery import shared_task
from django.core.management import call_command


@shared_task
def block_booking():
    call_command('block_booking')
