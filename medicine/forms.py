from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import (
    DoctorCheck,
    VosoritidRecord,
    VosoritidFirstRecord,
    RehabilitationRecord,
    Elongation,
    VosoritidPeriod
)

class DoctorCheckForm(forms.ModelForm):
    form_title = _('Каких врачей узких специальностей проходили')
    class Meta:
        model = DoctorCheck
        fields = '__all__'
        exclude = ['patient']

class VosoritidRecordForm(forms.ModelForm):
    form_title = _('Запись приема Восоритида')
    class Meta:
        model = VosoritidRecord
        fields = '__all__'
        exclude = ['user']

class VosoritidFirstRecordForm(forms.ModelForm):
    form_title = _('Запись первого приема Восоритида')
    class Meta:
        model = VosoritidFirstRecord
        fields = '__all__'
        exclude = ['user']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        today = timezone.now().date()

        if date and date >= today:
            raise ValidationError("Дата приема не может быть сегодняшней или будущей.")

        return cleaned_data

class RehabilitationRecordForm(forms.ModelForm):
    form_title = _('Укажите где проходите реабилитацию')
    class Meta:
        model = RehabilitationRecord
        fields = '__all__'
        exclude = ['profile']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y')}

class ElongationRecordForm(forms.ModelForm):
    form_title = _('Удлинение')
    class Meta:
        model = Elongation
        fields = '__all__'
        exclude = ['profile']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y')}

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        today = timezone.now().date()

        if date and date >= today:
            raise ValidationError("Дата процедуры не может быть сегодняшней или будущей.")

        return cleaned_data

class VosoritidPeriodRecordForm(forms.ModelForm):
    form_title = _('Период приема Восоритида')
    class Meta:
        model = VosoritidPeriod
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        today = timezone.now().date()

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("Дата начала приема должна быть раньше даты конца приема.")
            if end_date >= today:
                raise ValidationError("Дата конца приема не может быть сегодняшней или будущей.")

        return cleaned_data