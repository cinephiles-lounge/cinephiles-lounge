from django.urls import path
from . import views

urlpatterns = [
    path('', views.set_db),
    path('genre/', views.get_genre),
    path('list/', views.get_list),
    path('playing/', views.get_playing),
    path('upcoming/', views.get_upcoming),
]
