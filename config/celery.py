import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'blocking_flight_booking': {
        'task': 'flights.tasks.block_booking',
        'schedule': 60.0,
    }
}
