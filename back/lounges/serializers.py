from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from articles.serializers import ArticleSerializer

User = get_user_model()

class LoungeSerializer(serializers.ModelSerializer):
    class SimpleUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username', 'nickname', )

    admin = SimpleUserSerializer(read_only=True)
    members = SimpleUserSerializer(read_only=True, many=True)
    article_set = ArticleSerializer(read_only=True, many=True)

    class Meta:
        model = Lounge
        fields = '__all__'