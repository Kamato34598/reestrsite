from django import template
from django.contrib.auth import get_user_model

menu = [
    {'title': "Главная", 'slug': 'pages:index'},
    {'title': "Пациенты", 'slug': 'pages:patient_list'},
    {'title': "Отчеты", 'slug': 'pages:reports_list'},
    {'title': "Пользователи", 'slug': 'pages:users_list'},
    {'title': "Справочники", 'slug': 'pages:manual'},
    {'title': "Справка", 'slug': 'pages:reference'},
    {'title': "ОФ Маленький мир", 'slug': 'pages:about_us'},
    {'title': "О системе", 'slug': 'pages:about_system'},
]

register = template.Library()


@register.inclusion_tag('components/sidebar.html')
def show_sidebar(selected_menu=None):
    return {'menu': menu, 'selected_menu': selected_menu}

