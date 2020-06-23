from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat-room/<str:room_name>/', views.room, name='room'),
    path('room/', views.room_id, name='room_id'),
    path('<int:pk>/', views.get_id, name='get_id'),
    path('create_room/', views.create_room, name='create_room'),
    path('addusers/<int:pk>/', views.add_users, name='add_users'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('change-setting/', views.changeSettings, name='change'),
    path('remove-user/<int:pk>/', views.remove_user, name='remove'),
]
