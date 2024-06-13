from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from .models import (
    Patient,
    Doctor,
    DoctorProfile,
    ChildAddition,
    AdultAddition,
    AdultProfile,
    ChildProfile
)
from medicine.models import DoctorCheck

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Логин'), widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

class PatientRegistrationForm(UserCreationForm):
    form_title = _('')
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'first_name', 'city', 'phone_number')

class ChildPatientRegistrationForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'first_name', 'city', 'phone_number')
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
            'last_name': 'Фамилия ребенка',
            'first_name': 'Имя ребенка',
            'city': 'Город',
            'phone_number': 'Основной номер телефона'
        }

class CombinedAdultProfileForm(forms.ModelForm):
    class Meta:
        model = AdultProfile
        fields = ['IIN', 'birth_date', 'gender', 'height', 'disability', 'rehabilitation', 'medical_organization',
                  'diagnosis', 'vosoritid']
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y')}

    is_elongation = forms.BooleanField(label=_('Удлинение'), required=False)

    form_title = _('Профиль')

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height')
        is_elongation = cleaned_data.get('is_elongation')

        if height and is_elongation:
            if height < 150:
                raise ValidationError("Удлинение доступно только для пациентов с ростом выше 150 см.")

        return cleaned_data

    def save(self, commit=True):
        adult_profile = super().save(commit=False)
        adult_addition = AdultAddition(profile=adult_profile, is_elongation=self.cleaned_data['is_elongation'])

        if commit:
            adult_profile.save()
            adult_addition.save()

        return adult_profile
    def get_additional_data(self, pk=None):
        if pk is not None:
            additional_data = self.Meta.model.objects.get(pk=pk)
        else:
            additional_data = None
        return additional_data

class CombinedChildProfileForm(forms.ModelForm):
    class Meta:
        model = ChildProfile
        fields = ['IIN', 'birth_date', 'gender', 'height', 'disability', 'rehabilitation', 'medical_organization',
                  'diagnosis', 'vosoritid']
        labels = {
            'IIN': 'ИИН ребенка',
            'birth_date': 'Дата рождения ребенка',
            'gender': 'Пол ребенка',
            'height': 'Рост ребенка',
            'disability': 'Инвалидность',
            'rehabilitation': 'Проходите реабилитацию',
            'medical_organization': 'Медицинская организация',
        }
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y')}


    father_name = forms.CharField(label='ФИО отца', max_length=100, required=False)
    mother_name = forms.CharField(label='ФИО матери', max_length=100, required=False)
    father_number = forms.CharField(label='Номер телефона отца', max_length=16, required=False)
    mother_number = forms.CharField(label='Номер телефона матери', max_length=16, required=False)

    form_title = _('Профиль ребенка')
    def clean(self):
        cleaned_data = super().clean()
        father_name = cleaned_data.get('father_name')
        mother_name = cleaned_data.get('mother_name')

        if not father_name and not mother_name:
            raise ValidationError("Необходимо указать хотя бы одного родителя.")

        return cleaned_data

    def save(self, commit=True):
        child_profile = super().save(commit=False)
        child_addition = ChildAddition(profile=child_profile,
                                       father_name=self.cleaned_data['father_name'],
                                       mother_name=self.cleaned_data['mother_name'],
                                       father_number=self.cleaned_data['father_number'],
                                       mother_number=self.cleaned_data['mother_number'])

        if commit:
            child_profile.save()
            child_addition.save()

        return child_profile

    def get_additional_data(self, pk):
        additional_data = self.Meta.model.objects.get(pk=pk)
        return additional_data

class DoctorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'first_name', 'city')


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
        exclude = ('user',)

class DoctorCheckForm(forms.ModelForm):
    is_active = forms.BooleanField(required=False, initial=False)
    form_title = _('Каких врачей узких специальностей проходили')
    class Meta:
        model = DoctorCheck
        fields = ('doctor', 'is_active', 'date')
    def save(self, commit=True):
        if not self.cleaned_data.get('is_active', False):
            return None
        return super().save(commit=commit)

DoctorCheckFormSet = inlineformset_factory(ChildAddition, DoctorCheck, form=DoctorCheckForm, extra=8, can_delete=False)

