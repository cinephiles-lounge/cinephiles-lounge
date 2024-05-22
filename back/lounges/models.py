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


class LoungeArticle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_lounge_articles')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lounge = models.ForeignKey(Lounge, on_delete=models.CASCADE, related_name='articles')
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_lounge_articles')


class LoungeComment(models.Model):
    lounge_article = models.ForeignKey(LoungeArticle, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_lounge_comments')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_lounge_comments')
