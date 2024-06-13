from django.db import models
from django.utils.translation import gettext_lazy as _
from locations.models import Cities

class RehabilitationCenter(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название центра'))
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, related_name='rehabilitation_center', null=True, verbose_name=_('Город'))
    class Meta:
        verbose_name = _('Реабилитационный центр')
        verbose_name_plural = _('Реабилитационные центры')
        ordering = ['name']
    def __str__(self):
        return "{0}, {1}".format(self.name, self.city)

class MedicalOrganization(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Название'))
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name = _('Медицинская организация')
        verbose_name_plural = _('Медицинские организации')
    def __str__(self):
        return "{0}, {1}".format(self.name, self.city)

class Diagnosis(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Диагноз'))
    class Meta:
        verbose_name = _('Диагноз')
        verbose_name_plural = _('Диагнозы')

    def __str__(self):
        return self.name