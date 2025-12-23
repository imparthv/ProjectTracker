from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    # Extending djangos build in User using AbstractUser
    email = models.CharField(max_length=100, unique=True, blank=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username


