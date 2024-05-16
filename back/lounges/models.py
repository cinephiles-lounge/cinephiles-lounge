from django.db import models
from django.conf import settings
import uuid



class Lounge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_lounges')