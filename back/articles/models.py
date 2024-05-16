from django.db import models
from django.conf import settings
from movies.models import Movie
from lounges.models import Lounge
from django.core.validators import MinValueValidator, MaxValueValidator



class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_articles')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    rank = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lounge = models.ForeignKey(Lounge, on_delete=models.CASCADE, blank=True)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles')


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_comments')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments')
