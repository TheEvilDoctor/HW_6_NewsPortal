import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'new_post_in_category': {
        'task': 'NewsPortal.tasks.notify_about_new_post',
        'schedule': 30,
    }
}

app.conf.beat_schedule = {
    'weekly_notify_for_category_subs': {
        'task': 'NewsPortal.tasks.weekly_notify_subscribers',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
    }
}
