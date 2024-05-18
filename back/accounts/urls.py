from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/<int:to_user_pk>/', views.subscribe),
    path('liked_movies/', views.liked_movies),
]
