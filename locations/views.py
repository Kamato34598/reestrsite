from django.shortcuts import render, HttpResponse

menu = [
    #{'title': "Главная", 'url': ''},
    {'title': "Пациенты", 'url': ''},
    {'title': "Отчеты", 'url': ''},
    {'title': "Пользователи", 'url': ''},
    {'title': "Справочники", 'url': ''},
    {'title': "Справка", 'url': ''},
    {'title': "ОФ Маленький мир", 'url': ''},
    {'title': "О системе", 'url': ''},
]

def index(request):
    return render(request, 'locations/index.html')
