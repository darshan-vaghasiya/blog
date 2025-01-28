from celery import Celery
from celery.schedules import crontab
import os

# Create a Celery instance
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
celery_apps = Celery('blog_project.settings')
celery_apps.config_from_object('django.conf:settings', namespace='CELERY')

# Celery beat schedule configurations
celery_apps.conf.beat_schedule = {
    'generate_daily_post_stats': {
        'task': 'blog.tasks.generate_daily_post_stats',
        'schedule': crontab(minute='0', hour='0'),
    }
}

celery_apps.autodiscover_tasks()
