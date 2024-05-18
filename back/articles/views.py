import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *



# 게시글 전체 목록 조회
@api_view(['GET'])
def get_article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 


# 게시글 생성
@api_view(['POST'])
def create_article(request, movie_id):
    if request.method == 'POST':
        movie = Movie.objects.get(movie_id=movie_id)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 게시글 조회
@api_view(['GET'])
def article_detail(request, article_pk):
    if request.method == 'GET':
        article = Article.objects.get(pk=article_pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 게시글 수정, 삭제
@api_view(['PUT', 'DELETE'])
def article_update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user.pk == article.user.pk:
        if request.method == 'PUT':
            serializer = ArticleSerializer(article, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        message = {
            'access denied': '작성자만 접근이 가능합니다.'
        }
        return Response(message, status=status.HTTP_403_FORBIDDEN)


# 게시글 좋아요
@api_view(['POST'])
def like_article(request, article_pk):
    if request.method == 'POST':
        article = Article.objects.get(pk=article_pk)
        if article.liked_users.filter(pk=request.user.pk):
            article.liked_users.remove(request.user)
        else:
            article.liked_users.add(request.user)
        data = {
            'like_count': article.liked_users.count()        
        }
        return Response(data, status=status.HTTP_200_OK)



            
