# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from djongo import models as djongo_models
from django.utils import timezone

class CustomUser(AbstractUser):
    role = models.CharField(max_length=100, choices=[('TA', 'Teaching Assistant'), ('Student', 'Student')], default='Student')
    class_field = models.CharField(max_length=100, default='CSE 330')

class QueueEntry(djongo_models.Model):
    name = djongo_models.CharField(max_length=100)
    question = djongo_models.TextField()
    location = djongo_models.CharField(max_length=100)
    in_queue = models.BooleanField(default=True)
    username = models.CharField(max_length=150, null=True) 
    creation_date = models.DateTimeField(default=timezone.now)
    assisting_ta = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name
