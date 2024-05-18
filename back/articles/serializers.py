from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'movie', 'lounge', 'liked_users', )