from django.contrib import admin

from medicine.models import (
    DoctorCheck,
    DoctorSpeciality,
    RehabilitationCenter,
    RehabilitationRecord,
    VosoritidRecord,
)
from .medicalmodel import MedicalOrganization, Diagnosis

class DoctorCheckAdmin(admin.ModelAdmin):
    list_display = ('profile', 'doctor', 'date')

class DoctorSpecialityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RehabilitationCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')

class RehabilitationRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'date')

class VosoritidRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'height')
    search_fields = ('date', 'height')

class VosoritidFirstRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'first_height', 'second_height')
    search_fields = ('date', 'first_height', 'second_height')


admin.site.register(VosoritidRecord, VosoritidRecordAdmin)
admin.site.register(RehabilitationRecord, RehabilitationRecordAdmin)
admin.site.register(RehabilitationCenter, RehabilitationCenterAdmin)
admin.site.register(DoctorSpeciality, DoctorSpecialityAdmin)
admin.site.register(DoctorCheck, DoctorCheckAdmin)
admin.site.register(MedicalOrganization)
admin.site.register(Diagnosis)
