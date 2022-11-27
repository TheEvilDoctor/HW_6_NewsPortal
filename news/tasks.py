from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import *
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from NewsPortal import settings
from django.dispatch import receiver
from django.db.models.signals import m2m_changed


def send_notification_new(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_notification_weekly(subscribers, category, posts):
    html_content = render_to_string(
        'weekly_notif.html',
        {
            'category': category,
            'link': f'{settings.SITE_URL}/categories/{category.pk}',
            'news': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject=category,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notification_new(instance.preview(), instance.pk, instance.title, subscribers)


@shared_task
def weekly_notify_subscribers(sender, instance):
    date_to = datetime.now().date()
    date_from = timedelta(days=7)
    all_posts = Post.objects.filter(dateCreation__range=(date_from, date_to))
    all_categories = Category.objects.all
    for category in all_categories:
        posts = all_posts.filter(postCategory=category)
        subscribers = category.subscribers.all
        send_notification_weekly(subscribers, instance.category, posts)
