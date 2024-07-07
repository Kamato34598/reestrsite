from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    ResUser,
    AdultPatient,
    ChildPatient,
    ChildProfile,
    AdultProfile,
    AdultAddition,
    ChildAddition,
    Doctor,
    DoctorProfile,
)
from medicine.models import VosoritidFirstRecord, Elongation, RehabilitationRecord
from django.utils.translation import gettext_lazy as _
import nested_admin



class RehabilitationStackedInline(nested_admin.NestedStackedInline):
    model = RehabilitationRecord
    can_delete = False
    extra = 0
    max_num = 1
    verbose_name = _('Запись о реабилитации')
    verbose_name_plural = _('Запись о реабилитации')

class ElongationStackedInline(nested_admin.NestedStackedInline):
    model = Elongation
    extra = 0
    max_num = 1
    verbose_name = _('Удлинение')
    verbose_name_plural = _('Удлинения')

class AdultAdditionStackedInline(nested_admin.NestedStackedInline):
    inlines = [ElongationStackedInline]
    model = AdultAddition
    can_delete = False
    verbose_name = _('Дополнительная информация о пациенте')
    verbose_name_plural = _('Дополнительная информация о пациенте')


class PatientProfileAdmin(nested_admin.NestedModelAdmin):
    inlines = [AdultAdditionStackedInline, RehabilitationStackedInline]
    model = AdultProfile
    max_num = 1
    can_delete = False
    verbose_name = _('Профиль пациента')
    verbose_name_plural = _('Профили пациентов')

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user', 'is_child')  # Поля, которые должны быть только для чтения при редактировании
        else:
            return ()

    def has_delete_permission(self, request, obj=None):
        return False

class PatientProfileInline(StackedInline):
    model = AdultProfile
    can_delete = False
    verbose_name = _('Профиль пациента')
    verbose_name_plural = _('Профили пациентов')
    fieldsets = (
        (None, {
            'fields': ('gender', 'height')
        }),
        ('Медицинская информация', {
            'fields': ('medical_organization', 'diagnosis', 'vosoritid', 'disability', 'rehabilitation')
        }),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'gender', 'height', 'disability', 'rehabilitation', 'medical_organization', 'diagnosis',
                       'vosoritid')
        }),
    )


class PatientAdmin(BaseUserAdmin):
    inlines = (PatientProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    autocomplete_fields = ['city']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'birth_date', 'IIN', 'phone_number', 'city')}),
    )
    add_fieldsets = (
        (
            None, {
                'fields': (
                    'email',
                    'username',
                    'password1',
                    'password2'
                )
            }
        ), (
            'Личная информация', {
                'fields': (
                    'first_name',
                    'last_name',
                    'birth_date',
                    'IIN',
                    'phone_number',
                    'city'
                )
            }
        )
    )


class VosoritidFirstRecordAdmin(nested_admin.NestedStackedInline):
    model = VosoritidFirstRecord
    can_delete = False
    extra = 0
    max_num = 1
    verbose_name = _('Запись первого приема восоритида')
    verbose_name_plural = _('Записи первого приема восоритида')

class ChildAdditionStackedInline(nested_admin.NestedStackedInline):
    inlines = [VosoritidFirstRecordAdmin]
    model = ChildAddition
    can_delete = False
    verbose_name = _('Дополнительная информация ребенка')
    verbose_name_plural = _('Дополнительная информация ребенка')

class PatientChildProfileAdmin(nested_admin.NestedModelAdmin):
    inlines = [ChildAdditionStackedInline, RehabilitationStackedInline]
    model = ChildProfile
    can_delete = False
    verbose_name = _('Профиль ребенка пациента')
    verbose_name_plural = _('Профили детей пациентов')

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user', 'is_child')  # Поля, которые должны быть только для чтения при редактировании
        else:
            return ()

    def has_delete_permission(self, request, obj=None):
        return False

class PatientChildProfileInline(StackedInline):
    model = ChildProfile
    can_delete = False
    verbose_name = _('Профиль ребенка пациента')
    verbose_name_plural = _('Профили детей пациентов')

    fieldsets = (
        (None, {
            'fields': ('gender', 'height')
        }),
        ('Медицинская информация', {
            'fields': ('medical_organization', 'diagnosis', 'vosoritid', 'disability', 'rehabilitation')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'gender', 'height', 'disability', 'rehabilitation', 'medical_organization', 'diagnosis',
                       'vosoritid')
        }),
    )


class PatientChildAdmin(BaseUserAdmin):
    inlines = [PatientChildProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    autocomplete_fields = ['city']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'birth_date', 'IIN', 'phone_number', 'city')}),
    )
    add_fieldsets = (
        (
            None, {
                'fields': (
                    'email',
                    'username',
                    'password1',
                    'password2'
                )
            }
        ), (
            'Личная ифнормация', {
                'fields': (
                    'first_name',
                    'last_name',
                    'birth_date',
                    'IIN',
                    'phone_number',
                    'city'
                )
            }
        )
    )

class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False
    verbose_name = _('Профиль врача')
    verbose_name_plural = _('Профили врачей')



class DoctorAdmin(BaseUserAdmin):
    inlines = (DoctorProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    autocomplete_fields = ['city']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'birth_date', 'IIN', 'phone_number', 'city')}),
    )
    add_fieldsets = (
        (
            None, {
                'fields': (
                    'email',
                    'username',
                    'password1',
                    'password2'
                )
            }
        ), (
            'Личная информация', {
                'fields': (
                    'first_name',
                    'last_name',
                    'birth_date',
                    'IIN',
                    'phone_number',
                    'city'
                )
            }
        )
    )


class UserCustomerAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')




admin.site.register(ResUser ,UserCustomerAdmin)
admin.site.register(AdultPatient, PatientAdmin)
admin.site.register(ChildPatient, PatientChildAdmin)
admin.site.register(ChildProfile, PatientChildProfileAdmin)
admin.site.register(AdultProfile, PatientProfileAdmin)
admin.site.register(Doctor, DoctorAdmin)

