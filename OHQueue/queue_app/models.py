# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from djongo import models as djongo_models

class CustomUser(AbstractUser):
    role = models.CharField(max_length=100, choices=[('TA', 'Teaching Assistant'), ('Student', 'Student')], default='Student')

class QueueEntry(djongo_models.Model):
    name = djongo_models.CharField(max_length=100)
    question = djongo_models.TextField()
    location = djongo_models.CharField(max_length=100)
    in_queue = models.BooleanField(default=True)

    def __str__(self):
        return self.name
