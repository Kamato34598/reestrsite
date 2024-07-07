from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from locations.models import Cities
from medicine.medicalmodel import MedicalOrganization, Diagnosis
from .validators import validate_iin
import random


class Gender(models.TextChoices):
    MALE = 'male', _('мужской')
    FEMALE = 'female', _('женский')

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("You have not provided a valid username")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None ,email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('IIN', '999999{0}'.format(random.randint(100000, 999999)))
        extra_fields.setdefault('birth_date', timezone.now())
        return self._create_user(username, email, password, **extra_fields)

class ResUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=False, default='', unique=True)
    username = models.CharField(max_length=255, blank=False, default='', unique=True, verbose_name=_('Логин'))
    first_name = models.CharField(max_length=255, blank=False, default='', verbose_name=_('Имя'))
    last_name = models.CharField(max_length=255, blank=False, default='', verbose_name=_('Фамилия'))
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, verbose_name=_('Город'), related_name='users')
    phone_number = models.CharField(max_length=12, unique=True,verbose_name=_('Номер телефона'))
    IIN = models.CharField(max_length=12, unique=True, verbose_name=_('ИИН'), validators=[validate_iin])
    birth_date = models.DateField(verbose_name=_('Дата рождения'))

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username or self.email.split('@')[0]
    def __str__(self):
        return "{0} {1}".format(self.last_name, self.first_name)

class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(is_patient=True)

class Patient(ResUser):
    is_patient = True
    objects = PatientManager()

    class Meta:
        proxy = True
        verbose_name = _('Пациент')
        verbose_name_plural = _('Пациенты')

    def save(self, *args, **kwargs):
        self.is_patient = True
        super().save(*args, **kwargs)

class AdultPatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        patient_profile = PatientAltProfile.objects.filter(is_child=False)
        return results.filter(patient_altprofile__in=patient_profile)

class AdultPatient(ResUser):
    is_patient = True
    objects = AdultPatientManager()
    class Meta:
        proxy = True
        verbose_name = _('Пациент')
        verbose_name_plural = _('Пациенты')

class ChildPatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        patient_profile = PatientAltProfile.objects.filter(is_child=True)
        return results.filter(patient_altprofile__in=patient_profile)

class ChildPatient(ResUser):
    is_patient = True
    objects = ChildPatientManager()
    class Meta:
        proxy = True
        verbose_name = _('Пациент-ребенок')
        verbose_name_plural = _('Пациенты дети')

class PatientAltProfile(models.Model):
    user = models.OneToOneField(ResUser, on_delete=models.CASCADE, related_name='patient_altprofile')
    gender = models.CharField(verbose_name=_('Пол'), max_length=10, choices=Gender.choices)
    height = models.PositiveIntegerField(verbose_name=_('Рост'))
    disability = models.BooleanField(verbose_name=_('Инвалидность'), default=False)
    rehabilitation = models.BooleanField(verbose_name=_('Реабилитация'), default=False)
    medical_organization = models.ForeignKey(MedicalOrganization, on_delete=models.PROTECT, verbose_name=_('Медицинская организация'))
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.PROTECT, verbose_name=_('Диагноз'), related_name='patient_altprofile')
    vosoritid = models.BooleanField(verbose_name=_('Принимали Восоритид'), default=False)
    is_child = models.BooleanField(
        verbose_name=_('Личный статус'),
        default=False,
        choices=[(True, _('Ребенок')), (False, _('Взрослый'))]
    )

    class Meta:
        verbose_name = _('Профиль пациента')
        verbose_name_plural = _('Профили пациентов')

    def __str__(self):
        return "{0} {1}".format(_('Пациент:'), self.user)

class ChildProfileManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(is_child=True)

class ChildProfile(PatientAltProfile):
    is_child = True
    objects = ChildProfileManager()
    class Meta:
        proxy = True
        verbose_name = _('Профиль ребенка')
        verbose_name_plural = _('Профили детей')

    def save(self, *args, **kwargs):
        self.is_child = True  # Устанавливаем значение is_child при сохранении
        super().save(*args, **kwargs)

class AdultProfileManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(is_child=False)

class AdultProfile(PatientAltProfile):
    is_child = False
    objects = AdultProfileManager()
    class Meta:
        proxy = True
        verbose_name = _('Профиль пациента')
        verbose_name_plural = _('Профили пациентов')

class ChildAddition(models.Model):
    profile = models.OneToOneField(ChildProfile, on_delete=models.CASCADE, related_name='ChildAddition')
    father_name = models.CharField(verbose_name=_('ФИО отца'), max_length=100, blank=True, null=True)
    mother_name = models.CharField(verbose_name=_('ФИО матери'), max_length=100, blank=True, null=True)
    father_number = models.CharField(verbose_name=_('Номер телефона отца'), max_length=16, blank=True)
    mother_number = models.CharField(verbose_name=_('Номер телефона матери'), max_length=16, blank=True)
    class Meta:
        verbose_name = _('Дополнительная информация о родителях')
        verbose_name_plural = _('Дополнительная информация о родителях')

    def __str__(self):
        return "{0} {1}".format(self.profile, _('- дополнительная информация ребенка'))

class AdultAddition(models.Model):
    profile = models.OneToOneField(AdultProfile, on_delete=models.CASCADE, related_name='AdultAddition')
    is_elongation = models.BooleanField(default=False, verbose_name=_('Удлинение'))
    class Meta:
        verbose_name = _('Дополнительная информация пациента')
        verbose_name_plural = _('Дополнительная информация пациента')

    def __str__(self):
        return "{0} {1}".format(self.profile, _('- дополнительная информация пациента'))

class DoctorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(is_doctor=True)

class Doctor(ResUser):
    is_doctor = True
    objects = DoctorManager()

    class Meta:
        proxy = True
        verbose_name = _('Врач')
        verbose_name_plural = _('Врачи')

    def save(self, *args, **kwargs):
        self.is_doctor = True
        super().save(*args, **kwargs)

class DoctorProfile(models.Model):
    user = models.OneToOneField(ResUser, on_delete=models.CASCADE)
    is_proved = models.BooleanField(default=False, verbose_name=_('Подтвержден'))
    speciality = models.CharField(verbose_name=_('Специализация'), max_length=100, blank=True)