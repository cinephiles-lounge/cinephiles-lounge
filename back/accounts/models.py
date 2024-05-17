from django.db import models
from django.contrib.auth.models import AbstractUser
from lounges.models import Lounge


class User(AbstractUser):
    subscriptions = models.ManyToManyField('self', symmetrical=False, related_name='subscribers')
    profile_path = models.ImageField(blank=True)
    nickname = models.CharField(max_length=30)
    