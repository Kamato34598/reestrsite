from django.urls import path, include
from .views import index, user_login, user_logout, user_register

app_name = 'user'
urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register')
]