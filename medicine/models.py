from django.db import models
from django.utils.translation import gettext_lazy as _
from locations.models import Cities
from user.models import ResUser, ChildAddition, AdultAddition
from .medicalmodel import RehabilitationCenter

# Create your models here.

class RehabilitationRecord(models.Model):
    user = models.ForeignKey(ResUser, on_delete=models.CASCADE,related_name='rehabilitation_record')
    name = models.ForeignKey(RehabilitationCenter, on_delete=models.PROTECT,related_name='rehabilitation_record', verbose_name=_('Название центра'))
    date = models.DateField(verbose_name=_('Дата'))
    class Meta:
        verbose_name = _('Запись реабилитационного центра')
        verbose_name_plural = _('Записи реабилитационного центра')
        ordering = ['user']
        unique_together = ('user', 'date')

class VosoritidFirstRecord(models.Model):
    user = models.OneToOneField(ChildAddition,on_delete=models.CASCADE,related_name='first_vosoritid')
    date = models.DateField(verbose_name=_('Дата первого укола'))
    first_height = models.PositiveIntegerField(verbose_name=_('Начальный рост'))
    second_height = models.PositiveIntegerField(verbose_name=_('Рост на момент регистрации'))
    class Meta:
        verbose_name = _('Запись первого приема восоритида')
        verbose_name_plural = _('Записи первого приема восоритида')
        ordering = ['user']

class VosoritidRecord(models.Model):
    user = models.ForeignKey(ChildAddition,on_delete=models.CASCADE,related_name='Vosoritid_record')
    date = models.DateField(verbose_name=_('Дата укола'))
    height = models.PositiveIntegerField(verbose_name=_('Рост'))
    humerus_size = models.PositiveIntegerField(verbose_name=_('Размер плечевой кости'))
    forearm_size = models.PositiveIntegerField(verbose_name=_('Размер предплечья'))
    femur_size = models.PositiveIntegerField(verbose_name=_('Размер бедренной кости'))
    shin_size = models.PositiveIntegerField(verbose_name=_('Размер голени'))
    class Meta:
        verbose_name = _('Запись приема восоритида')
        verbose_name_plural = _('Записи приема восоритида')
        ordering = ['user']

class DoctorSpeciality(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('Специалист'))
    class Meta:
        verbose_name = _('Специалист')
        verbose_name_plural = _('Специалисты')
        ordering = ['name']
    def __str__(self):
        return self.name

class DoctorCheck(models.Model):
    profile = models.ForeignKey(ChildAddition, on_delete=models.CASCADE,related_name='doctor_check')
    doctor = models.ForeignKey(DoctorSpeciality, on_delete=models.CASCADE,related_name='doctor_check', verbose_name=_('Специалист'))
    date = models.DateField(verbose_name=_('Дата приема'))
    class Meta:
        verbose_name = _('Запись о приеме врача')
        verbose_name_plural = _('Записи о приеме врача')
        ordering = ['profile']
        unique_together = ('profile', 'date')

class Elongation(models.Model):
    profile = models.OneToOneField(AdultAddition, on_delete=models.CASCADE, related_name='elongation')
    date = models.DateField(verbose_name=_('Дата удлинения'))
    fragments = models.TextField(verbose_name=_('Какие фрагменты'))
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, related_name='Город')
    organization = models.CharField(max_length=100, verbose_name=_('Медучреждение'))
    class Meta:
        verbose_name = _('Удлинение')
        verbose_name_plural = _('Удлинения')

class VosoritidPeriod(models.Model):
    profile = models.OneToOneField(AdultAddition, on_delete=models.CASCADE, related_name='vosoritid_period')
    start_date = models.DateField(verbose_name=_('Дата начала приема'))
    end_date = models.DateField(verbose_name=_('Дата конца приема'))
    class Meta:
        verbose_name = _('Период приема Восоритида пациентом')
        verbose_name_plural = _('Периоды приема Восоритида пациентом')