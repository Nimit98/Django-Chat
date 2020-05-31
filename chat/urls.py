from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat-room/<str:room_name>/', views.room, name='room'),
    path('room', views.room_id, name='room_id'),
    path('<int:pk>/', views.get_id, name='get_id'),
]
