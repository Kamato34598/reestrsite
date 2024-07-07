from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, HttpResponse

from user.models import Patient#, PatientProfile, PatientChild, PatientChildProfile


@login_required(login_url='/login/')
def index(request):
    context = {
        'title': 'Реестр пациентов с редкими скелетными дисплазиями',
    }
    return render(request, 'pages/index.html', context=context)


@login_required(login_url='/login/')
def reports_list(request):
    context = {
        'title': 'Отчеты',
    }
    return render(request, 'pages/report_list.html', context=context)


@login_required(login_url='/login/')
def users_list(request):
    context = {
        'title': 'Пользователи',
    }
    return render(request, 'pages/users_list.html', context=context)


@login_required(login_url='/login/')
def user_detail(request, user_id):
    context = {
        'title': 'Профиль пользователя',
    }
    return render(request, '', context=context)


@login_required(login_url='/login/')
def manual(request):
    context = {
        'title': 'Справочники',
    }
    return render(request, 'pages/manual.html', context=context)


@login_required(login_url='/login/')
def reference(request):
    context = {
        'title': 'Справка',
    }
    return render(request, 'pages/reference.html', context=context)


@login_required(login_url='/login/')
def about_us(request):
    context = {
        'title': 'ОФ Маленький мир',
    }
    return render(request, 'pages/about_us.html', context=context)


@login_required(login_url='/login/')
def about_system(request):
    context = {
        'title': 'О системе',
    }
    return render(request, 'pages/about_system.html', context=context)
