from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from movies.serializers import MovieSerializer
from django.core.exceptions import ValidationError



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
            lounge_data = serializer.save(admin=request.user)
            lounge = Lounge.objects.get(id=lounge_data.id)
            lounge.members.add(request.user)
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
    

# 라운지 회원들이 좋아요 누른 영화 목록 조회
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def member_liked_movies(request, lounge_pk):
    if request.method == 'GET':
        lounge = Lounge.objects.get(pk=lounge_pk)
        members = lounge.members.all()

        movies = []
        movies_id_set = set()

        for member in members:
            person_movies = member.liked_movies.all()

            for movie in person_movies:
                curr_len = len(movies_id_set)
                movies_id_set.add(movie)
                if curr_len != len(movies_id_set):
                    movies.append(movie)
                    
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
