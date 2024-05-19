from django.db import models
from django.conf import settings
import uuid



class Lounge(models.Model):
    name = models.CharField(max_length=50)
    # admin 유저는 admin 권한을 다른 사람에게 넘겨준 후에 탈퇴할 수 있음
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='managing_lounges')
    description = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_lounges')