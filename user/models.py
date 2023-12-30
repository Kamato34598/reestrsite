from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
#from locations.models import Cities


class IntValidator:
    ALLOWED_CHARS = "0123456789"
    code = 'IIN'
    def __init__(self, message=None):
        self.message = message if message else _("IIN must consist of numbers")

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})

class Gender(models.TextChoices):
    MALE = 'male', _('Male')
    FEMALE = 'female', _('Female')


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        PATIENT = 'patient', _('Patient')
        PATIENT_CHILD = 'patient_child', _('Patient Child')
        DOCTOR = 'doctor', _('Doctor')
    base_role = Role.ADMIN
    role = models.CharField(_('Role'), max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super(User, self).save(*args, **kwargs)

class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PATIENT)

class Patient(User):
    base_role = User.Role.PATIENT

    patient = PatientManager()

    class Meta:
        proxy = True
        verbose_name = _('Пациент')
        verbose_name_plural = _('Пациенты')

@receiver(post_save, sender=Patient)
def create_patient_profile(sender, instance, created, **kwargs):
    if created and instance.role == "PATIENT":
        PatientProfile.objects.create(user=instance)

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IIN = models.CharField(verbose_name=_('ИИН'), max_length=12, unique=True)
    gender = models.CharField(verbose_name=_('Пол'), max_length=10, choices=Gender.choices)
    height = models.IntegerField(verbose_name=_('Рост'))
    disability = models.BooleanField(verbose_name=_('Инвалидность'), default=False)
    reabilitation = models.BooleanField(verbose_name=_('Реабилитация'), default=False)
    date_of_birth = models.DateField(verbose_name=_('Дата рождения'), blank=True, null=True)
#    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, verbose_name=_('Город'))

class PatientChildManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PATIENT_CHILD)

class PatientChild(User):
    base_role = User.Role.PATIENT_CHILD

    child_patient = PatientChildManager()

    class Meta:
        proxy = True
        verbose_name =_('Пациент-ребенок')
        verbose_name_plural =_('Дети пациенты')

@receiver(post_save, sender=PatientChild)
def create_patient_child_profile(sender, instance, created, **kwargs):
    if created and instance.role == "PATIENT_CHILD":
        PatientChildProfile.objects.create(user=instance)


class PatientChildProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IIN = models.CharField(verbose_name=_('ИИН ребенка'), max_length=12, unique=True)
    gender = models.CharField(verbose_name=_('Пол ребенка'), max_length=10, choices=Gender)
    father_name = models.CharField(verbose_name=_('ФИО отца'), max_length=100, blank=True)
    mother_name = models.CharField(verbose_name=_('ФИО матери'), max_length=100, blank=True)
    date_of_birth = models.DateField(verbose_name=_('Дата рождения ребенка'), blank=True, null=True)
    father_number = models.CharField(verbose_name=_('Номер телефона отца'), max_length=16, blank=True)
    mother_number = models.CharField(verbose_name=_('Номер телефона матери'), max_length=16, blank=True)
    disability = models.BooleanField(verbose_name=_('Инвалидность'))
    reabilitation = models.BooleanField(verbose_name=_('Реабилитация'))
#    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, verbose_name='Город')


class DoctorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DOCTOR)

class Doctor(User):
    base_role = User.Role.DOCTOR
    doctor = DoctorManager()

    class Meta:
        proxy = True
        verbose_name = _('Врач')
        verbose_name_plural = _('Врачи')

@receiver(post_save, sender=Doctor)
def create_doctor_profile(sender, instance, created, **kwargs):
    if created and instance.role == "DOCTOR":
        DoctorProfile.objects.create(user=instance)

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(verbose_name=_('Специализация'), max_length=100, blank=True)

