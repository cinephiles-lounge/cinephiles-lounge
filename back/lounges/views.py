from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *



@api_view(['GET'])
def get_lounge_list(request):
    if request.method == 'GET':
        lounges = Lounge.objects.all()
        serializer = LoungeSerializer(lounges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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


@api_view(['GET'])
def get_lounge_detail(request, lounge_pk):
    if request.method == 'GET':
        lounge = Lounge.objects.get(pk=lounge_pk)
        serializer = LoungeSerializer(lounge)
        return Response(serializer.data, status=status.HTTP_200_OK)