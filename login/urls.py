from . import views
from django.urls import path

app_name = 'login'

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
