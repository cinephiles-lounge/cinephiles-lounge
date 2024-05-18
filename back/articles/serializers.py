from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()


class CommentDetailSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='liked_users.count', read_only=True)

    class Meta:
        model = Comment
        exclude = ('article', )


class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentDetailSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='liked_users.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'movie', 'lounge', 'liked_users', )