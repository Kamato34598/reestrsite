from django.db.models import F
from django.shortcuts import render, HttpResponse

from user.models import Patient#, PatientProfile, PatientChild, PatientChildProfile


def index(request):
    context = {
        'title': 'Реестр пациентов с редкими скелетными дисплазиями',
    }
    return render(request, 'pages/index.html', context=context)

def patient_list(request):
    if request.method == 'GET':
        name = request.GET.get('lastName')
        gender = request.GET.get('gender')
        disability = request.GET.get('disability')
        print(name)
        print(gender)
        print(disability)
        patient = Patient.objects.filter(last_name=name)
        print(patient)
        # print(patient[0].patient_profile.height)
        # results = (
        #     list(PatientProfile.objects.filter(user__name__icontains=name).annotate(gender=F('gender')).values('disability', 'gender')) +
        #     list(PatientChildProfile.objects.filter(user__name__icontains=name).annotate(gender=F('gender')).values('disability', 'gender'))
        # )
    context = {
        'title': 'Пациенты',
    }
    return render(request, 'pages/patients.html', context=context)

def patient_detail(request, patient_id):
    context = {
        'title': 'Профиль пациента',
    }
    return render(request, '', context=context)

def patient_edit(request, patient_id):
    context = {
        'title': 'Редактирование профиля',
    }
    return render(request, '', context=context)

def reports_list(request):
    context = {
        'title': 'Отчеты',
    }
    return render(request, 'pages/report_list.html', context=context)

def users_list(request):
    context = {
        'title': 'Пользователи',
    }
    return render(request, 'pages/users_list.html', context=context)

def user_detail(request, user_id):
    context = {
        'title': 'Профиль пользователя',
    }
    return render(request, '', context=context)

def manual(request):
    context = {
        'title': 'Справочники',
    }
    return render(request, 'pages/manual.html', context=context)

def reference(request):
    context = {
        'title': 'Справка',
    }
    return render(request, 'pages/reference.html', context=context)

def about_us(request):
    context = {
        'title': 'ОФ Маленький мир',
    }
    return render(request, 'pages/about_us.html', context=context)

def about_system(request):
    context = {
        'title': 'О системе',
    }
    return render(request, 'pages/about_system.html', context=context)
