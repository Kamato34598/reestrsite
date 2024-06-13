from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

User = settings.AUTH_USER_MODEL

# @receiver(post_save, sender=Patient)
# def create_patient_profile(sender, instance, created, **kwargs):
#     if created and instance.is_patient:
#         PatientAltProfile.objects.create(user=instance)
#
# @receiver(post_save, sender=Patient)
# def create_patient_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "PATIENT":
#         PatientProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=PatientChild)
# def create_patient_child_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "PATIENT_CHILD":
#         PatientChildProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=Doctor)
# def create_doctor_profile(sender, instance, created, **kwargs):
#     if created and instance.is_doctor:
#         DoctorProfile.objects.create(user=instance)

