from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from login.views import user_login, user_logout, register, index


urlpatterns = [
    path('', index, name='index'),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
]
