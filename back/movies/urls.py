from django.urls import path
from . import views

urlpatterns = [
    path('', views.set_db),
    path('genre/', views.get_genre),
    path('list/', views.get_movie_list),
    path('playing/', views.get_playing),
    path('upcoming/', views.get_upcoming),
    path('recommend/like/', views.get_recommendation_like),
    path('recommend/weather/', views.get_recommendation_weather),
    path('<int:movie_id>/', views.get_movie_detail),
    path('<int:movie_id>/like/', views.like_movie),
    path('subs/', views.get_list_subscribing),
    path('short_review/create/<int:movie_id>/', views.create_short_review),
    path('short_review/<int:short_review_pk>/', views.update_short_review),
    path('search/', views.get_search),
]
