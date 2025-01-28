from django.db import models

from users.models import CustomUser, BaseModel


class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    category = models.CharField()
    comment_counts = models.IntegerField(default=0)
    like_counts = models.IntegerField(default=0)
    view_counts = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.title}"


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.post} --> {self.author}"


class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} --> {self.user}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.post.like_counts += 1
            self.post.save(update_fields=['like_counts'])

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.post.like_counts -= 1
        self.post.save(update_fields=['like_counts'])
        super().delete(*args, **kwargs)


class DailyPostStats(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='daily_posts_stats')
    like_counts = models.IntegerField(default=0)
    comment_counts = models.IntegerField(default=0)