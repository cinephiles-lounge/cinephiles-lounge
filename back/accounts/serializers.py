from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from movies.serializers import MovieSerializer
from articles.serializers import ArticleSerializer

class CustomRegisterSerializer(RegisterSerializer):
    # 닉네임 필드 추가
    # 회원가입 시에 필수로 작성하지 않아도 됨
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=30
    )

    def get_cleaned_data(self):
        username = self.validated_data.get('username', '')
        nickname = self.validated_data.get('nickname', '')
        # 만약 유저가 회원가입 시 닉네임을 입력하지 않았다면 닉네임은 username으로 자동 대체됨
        if not nickname:
            nickname = username
        return {
            'username': username,
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'nickname': nickname,
        }


class CustomUserDetailsSerializer(UserDetailsSerializer):
    liked_movies = MovieSerializer(many=True, read_only=True)
    liked_articles = ArticleSerializer(many=True, read_only=True)
    posted_articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        extra_fields = []
        if hasattr(User, 'USERNAME_FIELD'):
            extra_fields.append(User.USERNAME_FIELD)
        if hasattr(User, 'EMAIL_FIELD'):
            extra_fields.append(User.EMAIL_FIELD)
        if hasattr(User, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(User, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(User, 'nickname'):
            extra_fields.append('nickname')
        model = User
        fields = ('pk', 'liked_movies', 'liked_articles', 'posted_articles', *extra_fields)
        read_only_fields = ('email',)