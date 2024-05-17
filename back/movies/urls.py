from django.urls import path
from . import views

urlpatterns = [
    path('', views.set_db),
    path('genre/', views.get_genre),
    path('list/', views.get_list),
    path('playing/', views.get_playing),
    path('upcoming/', views.get_upcoming),
    path('recommend/like/', views.get_recommendation_like),
    path('<int:movie_pk>/', views.get_movie_detail),
    path('<int:movie_pk>/like/', views.movie_like),
]
