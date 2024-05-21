from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import *
from django.contrib.auth import get_user_model



User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname',)


class CommentSerializer(serializers.ModelSerializer):
    class SimpleArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('id', 'title', )

    user = SimpleUserSerializer(read_only=True)
    liked_users = SimpleUserSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    article = SimpleArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class SimpleCommentSerializer(serializers.ModelSerializer):
        like_count = serializers.IntegerField(source='liked_users.count', read_only=True)

        class Meta:
            model = Comment
            fields = ('id', 'user', 'content', 'created_at', 'like_count',)

    class SimpleMovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('movie_id', 'title')

    user = SimpleUserSerializer(read_only=True)
    comment_set = SimpleCommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    movie = SimpleMovieSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'liked_users', )


class SubscriptionUserSerializer(serializers.ModelSerializer):
    posted_articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'posted_articles', )
