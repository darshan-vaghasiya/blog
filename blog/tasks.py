import logging
from celery import shared_task
from django.utils import timezone
from .models import Post, Like, Comment, DailyPostStats

logger = logging.getLogger("my_custom_logger")


@shared_task
def generate_daily_post_stats():
    """
    Generate daily statistics for posts (like views, likes, and comments).
    """
    try:
        today = timezone.now().date()
        daily_posts = list()
        posts = Post.objects.filter(created_at__date=today)

        for post in posts:
            like_counts = Like.objects.filter(post=post, created_at__date=today).count()
            comment_counts = Comment.objects.filter(post=post, created_at__date=today).count()

            daily_posts.append(DailyPostStats(like_counts=like_counts, comment_counts=comment_counts, post=post))

        if daily_posts:
            DailyPostStats.objects.bulk_create(daily_posts)
    except Exception as e:
        logger.error(f"generate daily posts stats error = {e}")
