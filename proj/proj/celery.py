import os
from celery import Celery
from celery.schedules import crontab  # Для использования расписания с точностью до минут

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Настройка расписания Celery-Beat
app.conf.beat_schedule = {
    'send-emails-after-tournament-daily': {
        'task': 'courses.tasks.send_emails_after_tournament',  # путь к задаче
        'schedule': crontab(hour=0, minute=0),  # Ежедневно в полночь
    },
    'clearing-the-tournament-top-of-users-daily': {
        'task': 'courses.tasks.clearing_the_tournament_top_of_users',  # путь к задаче
        'schedule': crontab(hour=5, minute=0),  # Ежедневно в 5
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
