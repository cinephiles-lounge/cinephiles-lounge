from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_lounge_list),
    path('create/', views.create_lounge),
    path('<int:lounge_pk>/', views.get_lounge_detail),
]
