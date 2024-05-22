from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *
from articles.models import Article
from articles.serializers import ArticleSerializer
from movies.models import Movie
from movies.serializers import MovieSerializer
from django.core.exceptions import ValidationError
from django.db.models import Q, Count


# 전체 라운지 목록 조회
@api_view(['GET'])
def get_lounge_list(request):
    if request.method == 'GET':
        lounges = Lounge.objects.all()
        serializer = LoungeSerializer(lounges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 라운지 생성
# 멤버만 볼 수 있게 막아놔야 함
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_lounge(request):
    if request.method == 'POST':
        serializer = LoungeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 개별 라운지 상세 조회
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_lounge_detail(request, lounge_pk):
    if request.method == 'GET':
        lounge = Lounge.objects.get(pk=lounge_pk)
        serializer = LoungeSerializer(lounge)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 라운지 수정 / 삭제
@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE'])
def update_lounge(request, lounge_pk):
    lounge = Lounge.objects.get(pk=lounge_pk)
    if request.user.pk == lounge.admin.pk:
        if request.method == 'PUT':
            serializer = LoungeSerializer(lounge, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            lounge.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        message = {
            'message': '관리자만 접근 가능한 페이지입니다.'
        }
        return Response(message, status=status.HTTP_403_FORBIDDEN)
    

# 라운지 가입
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def join(request):
    if request.method == 'POST':
        try:
            if Lounge.objects.filter(uuid=request.data.get("code")).exists():
                lounge = Lounge.objects.get(uuid=request.data.get("code"))
                if lounge.members.filter(pk=request.user.pk).exists():
                    message = {
                        'message': '이미 가입한 라운지입니다.'
                    }
                    return Response(message, status=status.HTTP_409_CONFLICT)
                else:
                    lounge.members.add(request.user)
                    serializer = LoungeSerializer(lounge)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                message = {
                    'message': '일치하는 라운지 코드를 찾을 수 없습니다.'
                }
                return Response(message, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            message = {
                'message': '잘못된 코드 형식입니다.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
            

# 라운지 탈퇴
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def leave(request, lounge_pk):
    if request.method == 'POST':
        lounge = Lounge.objects.get(pk=lounge_pk)
        lounge.members.remove(request.user)
        serializer = LoungeSerializer(lounge)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 라운지 회원들이 좋아요 누른 영화 목록 조회 (회원 좋아요 순)
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def member_liked_movies(request, lounge_pk):
    if request.method == 'GET':
        lounge = Lounge.objects.get(pk=lounge_pk)
        members = lounge.members.all()
        member_liked_movies = Movie.objects.prefetch_related('liked_users').filter(liked_users__in=members).annotate(
            member_like_count=Count('liked_users', filter=Q(liked_users__in=members))
        ).order_by('-member_like_count')
        serializer = MovieSerializer(member_liked_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#############################################
#############################################
#############################################


# 라운지 회원들이 작성한 영화 리뷰 목록 조회
@api_view(['GET'])
def get_review_list(request, lounge_pk):
    if request.method == 'GET':
        lounge = Lounge.objects.get(pk=lounge_pk)
        if lounge.members.filter(pk=request.user.pk).exists() or lounge.admin.pk == request.user.pk:
            articles = Article.objects.filter(user__in=lounge.members.all()).order_by('-created_at')
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            message = {
                'message': '라운지 회원만 접근 가능한 페이지입니다.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)


# 라운지 게시글 전체 목록 조회
@api_view(['GET'])
def get_article_list(request, lounge_pk):
    if request.method == 'GET':
        lounge = Lounge.objects.get(pk=lounge_pk)
        if lounge.members.filter(pk=request.user.pk).exists() or lounge.admin.pk == request.user.pk:
            lounge_articles = lounge.articles.all().order_by('-created_at')
            serializer = LoungeArticleSerializer(lounge_articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            message = {
                'message': '라운지 회원만 접근 가능한 페이지입니다.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    

# 라운지 게시글 생성
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_article(request, lounge_pk):
    if request.method == 'POST':
        lounge = Lounge.objects.get(pk=lounge_pk)
        if lounge.members.filter(pk=request.user.pk).exists() or lounge.admin.pk == request.user.pk:
            serializer = LoungeArticleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, lounge=lounge)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            message = {
                'message': '라운지 회원만 접근 가능한 페이지입니다.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)


# 라운지 게시글 조회
@api_view(['GET'])
def article_detail(request, lounge_article_pk):
    if request.method == 'GET':
        lounge_article = LoungeArticle.objects.get(pk=lounge_article_pk)
        if lounge_article.lounge.members.filter(pk=request.user.pk).exists() or lounge_article.lounge.admin.pk == request.user.pk:
            serializer = LoungeArticleSerializer(lounge_article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            message = {
                'message': '라운지 회원만 접근 가능한 페이지입니다.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)


# 게시글 수정, 삭제
@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE'])
def article_update(request, article_pk):
    lounge_article = LoungeArticle.objects.get(pk=article_pk)
    if request.user.pk == lounge_article.user.pk:
        if request.method == 'PUT':
            serializer = LoungeArticleSerializer(lounge_article, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            lounge_article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        message = {
            'message': '작성자만 접근이 가능합니다.'
        }
        return Response(message, status=status.HTTP_403_FORBIDDEN)


# 게시글 좋아요
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def like_article(request, article_pk):
    if request.method == 'POST':
        lounge_article = LoungeArticle.objects.get(pk=article_pk)
        if lounge_article.lounge.members.filter(pk=request.user.pk).exists() or lounge_article.lounge.admin.pk == request.user.pk:
            if lounge_article.liked_users.filter(pk=request.user.pk):
                lounge_article.liked_users.remove(request.user)
            else:
                lounge_article.liked_users.add(request.user)
            data = {
                'like_count': lounge_article.liked_users.count()        
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            message = {
                'message': '라운지 회원만 접근 가능한 페이지입니다.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)



# 댓글 작성
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_comment(request, article_pk):
    lounge_article = LoungeArticle.objects.get(pk=article_pk)
    if request.method == 'POST':
        if lounge_article.lounge.members.filter(pk=request.user.pk).exists() or lounge_article.lounge.admin.pk == request.user.pk:
            lounge_article = LoungeArticle.objects.get(pk=article_pk)
            serializer = LoungeCommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, lounge_article=lounge_article)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            message = {
                'message': '라운지 회원만 접근 가능한 페이지입니다.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)
            

# 댓글 수정, 삭제
@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE'])
def update_comment(request, comment_pk):
    lounge_comment = LoungeComment.objects.get(pk=comment_pk)
    if request.user.pk == lounge_comment.user.pk:
        if request.method == 'PUT':
            serializer = LoungeCommentSerializer(lounge_comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            lounge_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        message = {
            'message': '작성자만 접근이 가능합니다.'
        }
        return Response(message, status=status.HTTP_403_FORBIDDEN)
