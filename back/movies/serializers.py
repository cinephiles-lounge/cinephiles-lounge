from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    
    class ShortReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShortReview
            fields = '__all__'
            read_only_fields = ('user', 'movie', )

    liked_users = UserSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)
    shortreview_set = ShortReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'