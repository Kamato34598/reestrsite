from django.db import models
from django.utils.translation import gettext_lazy as _

class Regions(models.Model):
    name = models.CharField(verbose_name=_('Назание области'), max_length=100)

    class Meta:
        verbose_name = _('Область')
        verbose_name_plural = _('Области')
        ordering = ['name']

    def __str__(self):
        return self.name

# class Districts(models.Model):
#     name = models.CharField(verbose_name=_('Название Района'), max_length=100)
#     region = models.ForeignKey(Regions, on_delete=models.PROTECT, verbose_name=_('Название области'))
#
#     class Meta:
#         verbose_name =_('Район')
#         verbose_name_plural = _('Районы')
#         ordering = ['name']
#     def __str__(self):
#         return self.name


class Cities(models.Model):
    name = models.CharField(verbose_name=_('Название города/села'), max_length=100)
    region = models.ForeignKey(Regions, on_delete=models.PROTECT, verbose_name=_('Название области'))
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        ordering = ['name']
    def __str__(self):
        return "{0}, город/село {1}".format(self.region.name,  self.name)
