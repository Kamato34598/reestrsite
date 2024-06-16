from django.urls import path, include
from .views import index, user_login, user_logout, user_register, TestWizard

app_name = 'user'
urlpatterns = [
    path('welcome/', index, name='index'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/<slug:patient_type>', user_register, name='register'),
    path('test/', TestWizard.as_view(), name='test'),
]