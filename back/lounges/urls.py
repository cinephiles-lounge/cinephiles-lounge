from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_lounge_list),
    path('create/', views.create_lounge),
    path('join/', views.join),
    path('<int:lounge_pk>/', views.get_lounge_detail),
    path('<int:lounge_pk>/update/', views.update_lounge),
    path('<int:lounge_pk>/leave/', views.leave),
    path('<int:lounge_pk>/movies/', views.member_liked_movies),
]
