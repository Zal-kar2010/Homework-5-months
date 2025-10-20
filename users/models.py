from django.contrib.auth.models import AbstractUser
from django.db import models
import random

def generate_confirmation_code():
    return str(random.randint(100000, 999999))  # 6-значный код

class User(AbstractUser):
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
