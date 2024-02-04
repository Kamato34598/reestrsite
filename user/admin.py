from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, PatientProfile, PatientChildProfile, PatientChild
from locations.models import Cities
from django.utils.translation import gettext_lazy as _



class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False
    verbose_name = _('Профиль пациента')
    verbose_name_plural = _('Профили пациентов')
    autocomplete_fields = ['city']


class PatientAdmin(BaseUserAdmin):
    inlines = [PatientProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        # ('Permissions', {'fields': ('is_active','groups',)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'city':
            kwargs['queryset'] = Cities.objects.select_related('district__region').order_by('district__region__name',
                                                                                            'district__name', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(PatientAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [PatientProfileInline]
        return super(PatientAdmin, self).change_view(*args, **kwargs)


class PatientChildProfileInline(admin.StackedInline):
    model = PatientChildProfile
    can_delete = False
    verbose_name = _('Профиль ребенка пациента')
    verbose_name_plural = _('Профили детей пациентов')

class PatientChildAdmin(BaseUserAdmin):
    inlines = [PatientChildProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Patient.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def add_view(self, *args, **kwargs):
        self.inlines= []
        return super(PatientChildAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines= [PatientChildProfileInline]
        return super(PatientChildAdmin, self).change_view(*args, **kwargs)

admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientChild, PatientChildAdmin)

