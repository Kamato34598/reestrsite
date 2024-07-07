from django.urls import path, include
from .views import index, user_login, user_logout, PatientRegisterWizard, ChildRegisterWizard, DoctorRegisterView, \
    ProfileView, register_page, patient_search_view, patient_detail, password_reset_request, password_reset_confirm

app_name = 'user'
urlpatterns = [
    path('welcome/', index, name='index'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path("reset/", password_reset_request, name="password_reset_request"),
    path("reset/<uidb64>/<token>/", password_reset_confirm, name="password_reset_confirm"),
    path('register/', register_page, name='register'),
    path('register_patient/', PatientRegisterWizard.as_view(), name='reg_patient'),
    path('register_child/', ChildRegisterWizard.as_view(), name='reg_child'),
    path('register_doctor/', DoctorRegisterView.as_view(), name='register_doctor'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('patients/', patient_search_view, name='patient_search'),
    path('patients/<int:pk>/', patient_detail, name='patient_profile'),
]