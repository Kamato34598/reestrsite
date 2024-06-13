# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import (
#     ResUser,
#     Patient,
#     PatientAltProfile,
#     AdultAddition,
#     ChildAddition,
#     Doctor,
#     DoctorProfile,
# )
# from medicine.models import VosoritidFirstRecord
# from django.utils.translation import gettext_lazy as _
# import nested_admin
#
# class AdultAdditionStackedInline(nested_admin.NestedStackedInline):
#
#
# class PatientProfileInline(admin.StackedInline):
#     model = PatientAltProfile
#     can_delete = False
#     verbose_name = _('Профиль пациента')
#     verbose_name_plural = _('Профили пациентов')
#
#
#
# class PatientAdmin(BaseUserAdmin):
#     inlines = (PatientProfileInline,)
#     list_display = ('username', 'email', 'first_name', 'last_name')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     list_filter = ('is_active',)
#     autocomplete_fields = ['city']
#
#     fieldsets = (
#         (None, {'fields': ('email', 'username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'city')}),
#         # ('Permissions', {'fields': ('is_active','groups',)}),
#     )
#     add_fieldsets = ((None, {'fields': ('email', 'username', 'password1', 'password2')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'city')}))
#
#
# class VosoritidFirstRecordAdmin(nested_admin.NestedStackedInline):
#     model = VosoritidFirstRecord
#     can_delete = False
#     verbose_name = _('Запись первого приема восоритида')
#     verbose_name_plural = _('Записи первого приема восоритида')
#
# class PatientChildProfileInline(nested_admin.NestedStackedInline):
#     inlines = [VosoritidFirstRecordAdmin]
#     model = PatientChildProfile
#     can_delete = False
#     verbose_name = _('Профиль ребенка пациента')
#     verbose_name_plural = _('Профили детей пациентов')
#
# class PatientChildAdmin(nested_admin.NestedModelAdmin):
#     inlines = [PatientChildProfileInline]
#     list_display = ('username', 'email', 'first_name', 'last_name')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     list_filter = ('is_active',)
#     autocomplete_fields = ['city']
#     fieldsets = (
#         (None, {'fields': ('email', 'username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'city')}),
#         # ('Permissions', {'fields': ('is_active','groups',)}),
#     )
#     add_fieldsets = ((None, {'fields': ('email', 'username', 'password1', 'password2')}),
#                      ('Personal info', {'fields': ('first_name', 'last_name', 'city')}))
#
# class DoctorProfileInline(admin.StackedInline):
#     model = DoctorProfile
#     can_delete = False
#     verbose_name = _('Профиль врача')
#     verbose_name_plural = _('Профили врачей')
#
#
#
# class DoctorAdmin(BaseUserAdmin):
#     inlines = (DoctorProfileInline,)
#     list_display = ('username', 'email', 'first_name', 'last_name')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     list_filter = ('is_active',)
#     autocomplete_fields = ['city']
#
#     fieldsets = (
#         (None, {'fields': ('email', 'username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'city')}),
#         # ('Permissions', {'fields': ('is_active','groups',)}),
#     )
#     add_fieldsets = ((None, {'fields': ('email', 'username', 'password1', 'password2')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'city')}))
#
#
# class UserCustomerAdmin(BaseUserAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'role')
#     search_fields = ('username', 'first_name', 'last_name')
#     readonly_fields = ('last_login','date_joined')
#
#
#
#
# admin.site.register(ResUser, UserCustomerAdmin)
# admin.site.register(Patient, PatientAdmin)
# admin.site.register(PatientChild, PatientChildAdmin)
# admin.site.register(Doctor, DoctorAdmin)

