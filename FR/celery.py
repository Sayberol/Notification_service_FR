import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FR.settings')

app = Celery('FR')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
