from django.urls import path, include
from .views import *

app_name = 'pages'
urlpatterns = [
    path('', index, name='index'),
    path('patients/', patient_list, name='patient_list'),
    path('patients/<int:pk>/', patient_detail, name='patient_detail'),
    path('report_list/', reports_list, name='reports_list'),
    path('users/', users_list, name='users_list'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
    path('manual/', manual, name='manual'),
    path('reference/', reference, name='reference'),
    path('about/', about_us, name='about_us'),
    path('system/', about_system, name='about_system'),
]