from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from movies.serializers import MovieSerializer
from .serializers import CustomUserDetailsSerializer


User = get_user_model()

# 회원 프로필 조회
# 좋아요 한 영화, 작성한 게시글, 좋아요 한 게시글을 모두 불러옴
@api_view(['GET'])
def get_user_detail(request, user_pk):
    if request.method == 'GET':
        user = User.objects.get(pk=user_pk)
        serializer = CustomUserDetailsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 회원정보 수정, 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_user_detail(request):
    if request.method == 'PUT':
        serializer = CustomUserDetailsSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 구독하기
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def subscribe(request, to_user_pk):
    if request.method == 'POST':
        if request.user.pk != to_user_pk:
            to_user = User.objects.get(pk=to_user_pk)
            if to_user.subscribers.filter(pk=request.user.pk).exists():
                to_user.subscribers.remove(request.user)
            else:
                to_user.subscribers.add(request.user)
            data = {
                'to_user_subscriber_count': to_user.subscribers.count(),
                'my_subscription_count': request.user.subscriptions.count()
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            message = {
                'message': '자기 자신은 구독할 수 없습니다.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    

# 내가 좋아요 한 영화 정보
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def liked_movies(request):
    if request.method == 'GET':
        movies = request.user.liked_movies.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    