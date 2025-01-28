from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('reader', 'Reader'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return f"{self.first_name} --> {self.last_name}"
