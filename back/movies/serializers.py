from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ShortReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortReview
        fields = '__all__'
        read_only_fields = ('user', 'movie', )


class MovieSerializer(serializers.ModelSerializer):
    liked_users = UserSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)
    shortreview_set = ShortReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class SubscriptionUserSerializer(serializers.ModelSerializer):
    liked_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'liked_movies')