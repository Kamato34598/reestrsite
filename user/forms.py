from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from locations.models import Cities, Regions
from medicine.medicalmodel import MedicalOrganization, Diagnosis
from .models import (
    Patient,
    Doctor,
    DoctorProfile,
    ChildAddition,
    AdultAddition,
    AdultProfile,
    ChildProfile, ResUser, PatientAltProfile
)
from medicine.models import DoctorCheck

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Логин'), widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(label=_('Новый пароль'), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_('Повторите пароль'), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")

        return cleaned_data

class PatientRegistrationForm(UserCreationForm):
    form_title = _('')
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'first_name', 'city', 'phone_number', 'IIN', 'birth_date')
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y')}

class ChildPatientRegistrationForm(UserCreationForm):
    form_title = _('')
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'first_name', 'city', 'phone_number', 'IIN', 'birth_date')
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
            'last_name': 'Фамилия ребенка',
            'first_name': 'Имя ребенка',
            'city': 'Город',
            'phone_number': 'Основной номер телефона',
            'IIN': 'ИИН ребенка',
            'birth_date': 'Дата рождения ребенка'
        }
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y')}


class CombinedAdultProfileForm(forms.ModelForm):
    class Meta:
        model = AdultProfile
        fields = ['gender', 'height', 'disability', 'rehabilitation', 'medical_organization',
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
        adult_profile = super().save(commit=commit)
        return adult_profile


class CombinedChildProfileForm(forms.ModelForm):
    class Meta:
        model = ChildProfile
        fields = ['gender', 'height', 'disability', 'rehabilitation', 'medical_organization',
                  'diagnosis', 'vosoritid']
        labels = {
            'gender': 'Пол ребенка',
            'height': 'Рост ребенка',
            'disability': 'Инвалидность',
            'rehabilitation': 'Проходите реабилитацию',
            'medical_organization': 'Медицинская организация',
        }


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
            raise ValidationError(_("Необходимо указать хотя бы одного родителя."))

        return cleaned_data

    def save(self, commit=True):
        child_profile = super().save()
        return child_profile

class DoctorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'first_name', 'city')


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ('speciality',)

class DoctorCheckForm(forms.ModelForm):
    is_active = forms.BooleanField(required=False, initial=False, label='', help_text=_('Отметье флажок если вы проходили этого специалиста'))
    form_title = _('Каких врачей узких специальностей проходили')
    class Meta:
        model = DoctorCheck
        fields = ('doctor', 'date', 'is_active',)
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y')}

    def clean(self):
        cleaned_data = super().clean()
        is_active = cleaned_data.get('is_active')
        date = cleaned_data.get('date')
        if is_active and not date:
            raise ValidationError(_("Нужно указать дату приема."))
        return cleaned_data

    def save(self, commit=True):
        if not self.cleaned_data.get('is_active', False):
            return None
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        super(DoctorCheckForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].widget.attrs['readonly'] = True

DoctorCheckFormSet = inlineformset_factory(ChildAddition, DoctorCheck, form=DoctorCheckForm, extra=8, can_delete=False)

class PatientUserEditForm(UserChangeForm):
    password = None
    class Meta:
        model = ResUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'IIN', 'city')

    def __init__(self, *args, **kwargs):
        super(PatientUserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True
        self.fields['birth_date'].widget.attrs['readonly'] = True
        self.fields['IIN'].widget.attrs['readonly'] = True

class PatientProfileEditForm(forms.ModelForm):
    class Meta:
        model = PatientAltProfile
        fields = ('gender', 'height', 'diagnosis', 'disability', 'medical_organization')

    def __init__(self, *args, **kwargs):
        super(PatientProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['readonly'] = True
        self.fields['height'].widget.attrs['readonly'] = True
        self.fields['diagnosis'].widget.attrs['readonly'] = True

class DoctorUserEditForm(UserChangeForm):
    password = None
    class Meta:
        model = ResUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'IIN', 'city')

    def __init__(self, *args, **kwargs):
        super(DoctorUserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True
        self.fields['birth_date'].widget.attrs['readonly'] = True
        self.fields['IIN'].widget.attrs['readonly'] = True

class PatientChildUserEditForm(UserChangeForm):
    password = None
    class Meta:
        model = ResUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'IIN', 'city')
        labels = {
            'first_name': _('Фамилия ребенка'),
            'last_name': _('Имя ребенка'),
            'birth_date': _('Дата рождения ребенка'),
            'IIN': _('ИИН ребенка')
        }

    def __init__(self, *args, **kwargs):
        super(PatientChildUserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True
        self.fields['birth_date'].widget.attrs['readonly'] =True
        self.fields['IIN'].widget.attrs['readonly'] =True

class ChildAdditionUpdateForm(forms.ModelForm):
    class Meta:
        model = ChildAddition
        fields = ('father_name', 'mother_name', 'father_number', 'mother_number')

    def __init__(self, *args, **kwargs):
        super(ChildAdditionUpdateForm, self).__init__(*args, **kwargs)
        self.fields['father_name'].widget.attrs['readonly'] = True
        self.fields['mother_name'].widget.attrs['readonly'] = True


class PatientChildProfileEditForm(forms.ModelForm):
    class Meta:
        model = PatientAltProfile
        fields = ('gender', 'diagnosis', 'disability', 'medical_organization')
        labels = {
            'gender': _('Пол ребенка'),
        }

    def __init__(self, *args, **kwargs):
        super(PatientChildProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['readonly'] = True
        self.fields['diagnosis'].widget.attrs['readonly'] = True

class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        model = ResUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'city')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

class PatientSearchForm(forms.Form):
    last_name = forms.CharField(label='Фамилия', required=False)
    birth_date = forms.DateField(label='Дата рождения', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(label='Пол', choices=[('', '---------'), ('male', _('мужской')), ('female', _('женский'))], required=False)
    is_child = forms.ChoiceField(label='Личный статус',
                                 choices=[('', '---------'), ('True', 'Ребенок'), ('False', 'Взрослый')],
                                 required=False)
    city = forms.ModelChoiceField(queryset=Cities.objects.all(), label='Город', required=False)
    region = forms.ModelChoiceField(queryset=Regions.objects.all(), label='Область', required=False)
    medical_organization = forms.ModelChoiceField(queryset=MedicalOrganization.objects.all(),
                                                  label='Медицинская организация', required=False)
    diagnosis = forms.ModelChoiceField(queryset=Diagnosis.objects.all(), label='Диагноз', required=False)
    rehabilitation = forms.ChoiceField(label='Реабилитация',
                                       choices=[('', '---------'), ('True', 'Да'), ('False', 'Нет')], required=False)
    disability = forms.ChoiceField(label='Инвалидность', choices=[('', '---------'), ('True', 'Да'), ('False', 'Нет')],
                                   required=False)
    vosoritid = forms.ChoiceField(label='Принимали Восоритид',
                                  choices=[('', '---------'), ('True', 'Да'), ('False', 'Нет')], required=False)
    def search(self):
        # Функция для выполнения поиска на основе предоставленных данных формы
        last_name = self.cleaned_data.get('last_name')
        birth_date = self.cleaned_data.get('birth_date')
        gender = self.cleaned_data.get('gender')
        is_child = self.cleaned_data.get('is_child')
        city = self.cleaned_data.get('city')
        region = self.cleaned_data.get('region')
        medical_organization = self.cleaned_data.get('medical_organization')
        diagnosis = self.cleaned_data.get('diagnosis')
        rehabilitation = self.cleaned_data.get('rehabilitation')
        disability = self.cleaned_data.get('disability')
        vosoritid = self.cleaned_data.get('vosoritid')

        # Создаем фильтр на основе переданных данных
        filters = {}
        if last_name:
            filters['user__last_name__icontains'] = last_name
        if birth_date:
            filters['user__birth_date'] = birth_date
        if gender:
            filters['gender'] = gender
        if is_child:
            filters['is_child'] = is_child
        if city:
            filters['user__city__icontains'] = city
        if region:
            filters['user__city__region__icontains'] = region
        if medical_organization:
            filters['medical_organization'] = medical_organization
        if diagnosis:
            filters['diagnosis'] = diagnosis
        if rehabilitation is not '':
            filters['rehabilitation'] = rehabilitation
        if disability is not '':
            filters['disability'] = disability
        if vosoritid is not '':
            filters['vosoritid'] = vosoritid
        # Выполняем запрос к базе данных и возвращаем результат
        return PatientAltProfile.objects.filter(**filters)
