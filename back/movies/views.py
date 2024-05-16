import requests
from django.shortcuts import render
from rest_framework.response import Response


def set_db(request):
    
    url = f''
    response = requests.get(url).json()
    return
