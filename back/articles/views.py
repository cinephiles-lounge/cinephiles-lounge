from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *
from datetime import date, timedelta


# 게시글 전체 목록 조회
@api_view(['GET'])
def get_article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 


# 게시글 생성
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_article(request, movie_id):
    if request.method == 'POST':
        movie = Movie.objects.get(movie_id=movie_id)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            # 라운지 정보가 존재할 시에는 유저가 해당 라운지의 회원인지 확인한 후 저장
            if request.data.get('lounge'):
                lounge = Lounge.objects.get(pk=request.data.get('lounge'))
                if lounge.members.filter(pk=request.user.pk).exists():
                    serializer.save(lounge=lounge)
                else:
                    message = {
                        'message': '가입한 라운지의 게시글만 작성이 가능합니다.'
                    }
                    return Response(message, status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 게시글 조회
@api_view(['GET'])
def article_detail(request, article_pk):
    if request.method == 'GET':
        article = Article.objects.get(pk=article_pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 게시글 수정, 삭제
@permission_classes([IsAuthenticated])
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
            'message': '작성자만 접근이 가능합니다.'
        }
        return Response(message, status=status.HTTP_403_FORBIDDEN)


# 게시글 좋아요
@permission_classes([IsAuthenticated])
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


# 댓글 작성
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_comment(request, article_pk):
    if request.method == 'POST':
        article = Article.objects.get(pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_200_OK)
            

# 댓글 수정, 삭제
@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE'])
def update_comment(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user.pk == comment.user.pk:
        if request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        message = {
            'message': '작성자만 접근이 가능합니다.'
        }
        return Response(message, status=status.HTTP_403_FORBIDDEN)


# 댓글 좋아요
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def like_comment(request, comment_pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_pk)
        if comment.liked_users.filter(pk=request.user.pk).exists():
            comment.liked_users.remove(request.user)
        else:
            comment.liked_users.add(request.user)
        
        data = {
            'like_count': comment.liked_users.count()
        }
        return Response(data, status=status.HTTP_200_OK)
    

# 내가 구독하는 사람들이 작성한 게시글 조회
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_list_subscribing(request):
    if request.method == 'GET':
        subscriptions = request.user.subscriptions.all()

        articles = []

        for subscribing_user in subscriptions:
            person_articles = subscribing_user.posted_articles.all()
            for article in person_articles:
                    articles.append(article)
                    
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 게시글 인기 순으로 조회
@api_view(['GET'])
def get_popular(request):
    if request.method == 'GET':
        articles = Article.objects.filter(
            # 최근 일주일 이내에 작성된 게시글만 불러오기
            created_at__gte=date.today()-timedelta(7)
        ).annotate(
            # 인기도(좋아요 + 댓글 수) 도출 후 내림차순으로 정렬
            popularity=Count('liked_users')+Count('comment')
        ).order_by('-popularity') 
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)