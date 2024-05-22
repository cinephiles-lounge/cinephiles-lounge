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
    ########## lounge article ############ 
    path('<int:lounge_pk>/articles/', views.get_article_list),
    path('<int:lounge_pk>/articles/create/', views.create_article),
    path('articles/<int:lounge_article_pk>/', views.article_detail),
    path('articles/<int:article_pk>/update/', views.article_update),
    path('articles/<int:article_pk>/like/', views.like_article),
    path('articles/<int:article_pk>/comment/create/', views.create_comment),
    path('comment/<int:comment_pk>/', views.update_comment),
]
