from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_user_detail),
    path('<int:user_pk>/', views.get_user_detail),
    path('subscribe/<int:to_user_pk>/', views.subscribe),
    path('liked_movies/', views.liked_movies),
    path('lounges/', views.get_joined_lounges),
    path('lounges/admin/', views.get_managing_lounges),
]
