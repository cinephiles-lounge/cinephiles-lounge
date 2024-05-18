from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class Genre(models.Model):
    genre_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)


class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    is_adult = models.BooleanField()
    title = models.CharField(max_length=100)
    overview = models.TextField()
    popularity = models.FloatField()
    release_date = models.DateField(blank=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200)
    trailer_key = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies')


class ShortReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_short_reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rank = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
