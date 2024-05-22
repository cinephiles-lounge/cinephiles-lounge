from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from articles.serializers import ArticleSerializer



User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname',)


class CommentSerializer(serializers.ModelSerializer):
    class SimpleLoungeArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = LoungeArticle
            fields = ('id', 'title', )

    user = SimpleUserSerializer(read_only=True)
    liked_users = SimpleUserSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    lounge_article = SimpleLoungeArticleSerializer(read_only=True)

    class Meta:
        model = LoungeComment
        fields = '__all__'


class LoungeArticleSerializer(serializers.ModelSerializer):
    class SimpleLoungeCommentSerializer(serializers.ModelSerializer):
        like_count = serializers.IntegerField(source='liked_users.count', read_only=True)
        user = SimpleUserSerializer(read_only=True)

        class Meta:
            model = LoungeComment
            fields = ('id', 'user', 'content', 'created_at', 'like_count',)
    
    user = SimpleUserSerializer(read_only=True)
    lounge_comment_set = SimpleLoungeCommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='liked_users.count', read_only=True)

    class Meta:
        model = LoungeArticle
        fields = '__all__'
        read_only_fields = ('user', 'liked_users', 'lounge' )


class LoungeSerializer(serializers.ModelSerializer):
    admin = SimpleUserSerializer(read_only=True)
    members = SimpleUserSerializer(read_only=True, many=True)
    lounge_article_set = LoungeArticleSerializer(read_only=True, many=True)

    class Meta:
        model = Lounge
        fields = '__all__'