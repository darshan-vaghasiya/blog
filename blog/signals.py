from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def update_comment_count(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.comment_counts += 1
        post.save(update_fields=['comment_counts'])
