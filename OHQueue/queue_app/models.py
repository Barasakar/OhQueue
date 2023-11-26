# models.py: this script extends the default Django and MongoDB User.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # added a role field to specify whether a user is a TA or a student.
    role = models.CharField(max_length=100, 
                            #(A, B) A is for machine readable(actual value in DB); B is human readable value.
                            choices=[('TA', 'Teaching Assistant'), ('Student', 'Student')], 
                            default='Student')
