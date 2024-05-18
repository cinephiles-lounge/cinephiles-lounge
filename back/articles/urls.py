from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_article_list),
    path('create/<int:movie_id>/', views.create_article),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/update/', views.article_update),
    path('<int:article_pk>/like/', views.like_article),
]
