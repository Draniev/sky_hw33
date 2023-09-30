from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    username
    email
    first_name
    last_name
    password
    """
    # username = models.CharField(max_length=64, unique=True)
    pass
