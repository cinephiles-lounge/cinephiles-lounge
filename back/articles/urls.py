from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_article_list),
    path('create/<int:movie_id>/', views.create_article),
    path('<int:article_pk>/like/', views.like_article),
]
