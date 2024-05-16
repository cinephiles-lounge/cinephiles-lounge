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

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('genre_id', )

    liked_users = UserSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, allow_null=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        # 영화가 이미 DB에 존재하면 popularity, vote_average, vote_count 등 변동 가능한 속성들의 데이터를 업데이트
        if Movie.objects.filter(movie_id=validated_data.get('movie_id')).exists():
            movie = Movie.objects.get(movie_id=validated_data.get('movie_id'))
            movie.popularity = validated_data.get('popularity')
            movie.vote_average = validated_data.get('vote_average')
            movie.vote_count = validated_data.get('vote_count')
        else:
            # 영화가 DB 존재하지 않는다면 Create
            genre_ids = validated_data.pop('genres')
            print(genre_ids)
            movie = Movie.objects.create(**validated_data)
            if genre_ids:
                for genre_id in genre_ids:
                    genre = Genre.objects.get(genre_id=genre_id)
                    movie.genres.add(genre)
            movie.save()
        return movie