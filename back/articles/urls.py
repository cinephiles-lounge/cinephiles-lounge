from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_article_list),
    path('create/<int:movie_id>/', views.create_article)
]
