from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

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