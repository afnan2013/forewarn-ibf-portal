from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    isPasswordChanged = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)