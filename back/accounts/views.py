from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from movies.serializers import MovieSerializer

User = get_user_model()

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def subscribe(request, to_user_pk):
    if request.method == 'POST':
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
    

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def liked_movies(request):
    if request.method == 'GET':
        movies = request.user.liked_movies.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    