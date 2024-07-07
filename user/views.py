import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes

from .utils import CustomLoginRequiredMixin
from django.views import View
from formtools.wizard.views import SessionWizardView
from django.utils.translation import gettext_lazy as _
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_encode, urlsafe_base64_decode
from medicine.models import Elongation, VosoritidPeriod, RehabilitationRecord, VosoritidFirstRecord, DoctorCheck, \
    VosoritidRecord
from .forms import (
    LoginForm,
    PatientRegistrationForm,
    ChildPatientRegistrationForm,
    CombinedAdultProfileForm,
    CombinedChildProfileForm,
    DoctorCreationForm,
    DoctorProfileForm,
    DoctorCheckFormSet, PatientChildUserEditForm, PatientChildProfileEditForm, DoctorUserEditForm,
    ChildAdditionUpdateForm, PatientUserEditForm, PatientProfileEditForm, UserEditForm, PatientSearchForm,
    PasswordResetRequestForm, SetPasswordForm
)
from medicine.forms import (
    ElongationRecordForm,
    VosoritidPeriodRecordForm,
    RehabilitationRecordForm,
    VosoritidRecordForm, VosoritidFirstRecordForm,
)
from .models import Patient, AdultProfile, AdultAddition, ChildAddition, PatientAltProfile, ResUser


def index(request):
    print(request.user.is_active)
    return render(request, 'user/index.html')


def user_login(request):
    if not request.user.is_authenticated:
        next_url = request.GET.get('next') or ''
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request,
                                    username=cd['username'],
                                    password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        next_url = request.POST.get('next') or None
                        if next_url:
                            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                                return redirect(next_url)
                            else:
                                return HttpResponse('Invalid next URL')
                        else:
                            return redirect('pages:index')

                    else:
                        return HttpResponse('Disabled account')
            else:
                context = {'form': form}
                return render(request, 'user/login.html', context)
        else:
            form = LoginForm()
        return render(request, 'user/login.html', {'form': form, 'next': next_url})
    else:
        return redirect('pages:index')


def user_logout(request):
    logout(request)
    return redirect('user:login')


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = ResUser.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    password_reset_url = request.build_absolute_uri(
                        f"/reset/{uid}/{token}/"
                    )
                    email_subject = "Запрос на сброс пароля"
                    email_body = render_to_string("user/password_reset_email.txt", {
                        'username': user.username,
                        'password_reset_url': password_reset_url,
                    })
                    send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [email])
                return redirect("password_reset_done")
    else:
        form = PasswordResetRequestForm()
    return render(request, "user/password_reset_form.html", {"form": form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = ResUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ResUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data["new_password1"]
                user.set_password(new_password)
                user.save()
                return redirect("password_reset_complete")
        else:
            form = SetPasswordForm()
    else:
        return redirect("password_reset_invalid")


def password_reset_done(request):
    return render(request, "user/password_reset_done.html")


def password_reset_complete(request):
    return render(request, "user/password_reset_complete.html")


def password_reset_invalid(request):
    return render(request, "user/password_reset_invalid.html")


def register_page(request):
    return render(request, 'user/register.html')


def get_my_form(form_class, form_list):
    for form_instance in form_list:
        if isinstance(form_instance, form_class):
            return form_instance
    return None


list_of_forms = {
    'patient': PatientRegistrationForm,
    'adultprofile': CombinedAdultProfileForm,
    'elongation': ElongationRecordForm,
    'vosoritid_period': VosoritidPeriodRecordForm,
    "rehab_record": RehabilitationRecordForm,
    'patient_child': ChildPatientRegistrationForm,
    'childprofile': CombinedChildProfileForm,
    'doctorcheck': DoctorCheckFormSet,
    'vosoritid_first': VosoritidFirstRecordForm,
}


class PatientRegisterWizard(SessionWizardView):
    template_name = 'user/basic_wizard_form.html'
    form_list = [
        ('patient', PatientRegistrationForm),
        ('adultprofile', CombinedAdultProfileForm),
        ('elongation', ElongationRecordForm),
        ('vosoritid_period', VosoritidPeriodRecordForm),
        ("rehab_record", RehabilitationRecordForm),
    ]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['form_title'] = form.form_title
        context['global_title'] = _('Регистрация пациента')
        self.get_form_list()
        return context

    def done(self, form_list, **kwargs):
        # Step 1: Save the patient
        patient_form = form_list[0]
        patient = patient_form.save()

        # Step 2: Save the adult profile
        adult_profile_form = form_list[1]
        adult_profile = adult_profile_form.save(commit=False)
        adult_profile.user = patient
        adult_profile.save()

        # Step 3: Save adult addition information
        is_elongation = adult_profile_form.cleaned_data['is_elongation']
        adult_addition = AdultAddition.objects.create(profile=adult_profile, is_elongation=is_elongation)

        # Step 4: Save elongation record if applicable
        if adult_profile_form.cleaned_data.get('is_elongation'):
            elongation_form = get_my_form(list_of_forms['elongation'], form_list=form_list)
            elongation = elongation_form.save(commit=False)
            elongation.profile = adult_addition
            elongation.save()
            print("elongation")

        # Step 5: Save Vosoritid period if applicable
        if adult_profile_form.cleaned_data.get('vosoritid'):
            vosoritid_period_form = get_my_form(list_of_forms['vosoritid_period'], form_list=form_list)
            vosoritid_period = vosoritid_period_form.save(commit=False)
            vosoritid_period.profile = adult_addition
            vosoritid_period.save()
            print("vosoritid")

        # Step 6: Save rehabilitation record if applicable
        if adult_profile_form.cleaned_data.get('rehabilitation'):
            rehab_record_form = get_my_form(list_of_forms['rehab_record'], form_list=form_list)
            rehab_record = rehab_record_form.save(commit=False)
            rehab_record.profile = adult_profile
            rehab_record.save()
            print("rehab")

        return redirect('user:login')

    def skip_rehabilitation_record(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('adultprofile') or {}
        return cleaned_data.get('rehabilitation', True)

    def skip_vosoritid(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('adultprofile') or {}
        return cleaned_data.get('vosoritid', True)

    def skip_elongation(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('adultprofile') or {}
        return cleaned_data.get('is_elongation', True)

    condition_dict = {
        'rehab_record': skip_rehabilitation_record,
        'vosoritid_period': skip_vosoritid,
        'elongation': skip_elongation,
    }


TEMPLATES = {
    'patient_child': 'user/basic_wizard_form.html',
    'childprofile': 'user/basic_wizard_form.html',
    'vosoritid_first': 'user/basic_wizard_form.html',
    'rehab_record': 'user/basic_wizard_form.html',
}


# регистрация без приема докторов
class ChildRegisterWizard(SessionWizardView):
    template_name = 'user/basic_wizard_form.html'
    form_list = [
        ('patient_child', ChildPatientRegistrationForm),
        ('childprofile', CombinedChildProfileForm),
        ('vosoritid_first', VosoritidFirstRecordForm),
        ('rehab_record', RehabilitationRecordForm),
    ]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['form_title'] = form.form_title
        context['global_title'] = _('Регистрация пациента ребенка')
        self.get_form_list()
        return context

    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        # Step 1: Save the child patient
        child_patient_form = form_list[0]
        child_patient = child_patient_form.save()

        # Step 2: Save the child profile
        child_profile_form = form_list[1]
        child_profile = child_profile_form.save(commit=False)
        child_profile.user = child_patient
        child_profile.save()
        father_name = child_profile_form.cleaned_data['father_name']
        mother_name = child_profile_form.cleaned_data['mother_name']
        father_number = child_profile_form.cleaned_data['father_number']
        mother_number = child_profile_form.cleaned_data['mother_number']
        child_addition = ChildAddition.objects.create(
            profile=child_profile,
            father_name=father_name,
            mother_name=mother_name,
            father_number=father_number,
            mother_number=mother_number
        )

        # Step 4: Save the Vosoritid first record if applicable
        if child_profile_form.cleaned_data.get('vosoritid'):
            vosoritid_first_form = get_my_form(list_of_forms['vosoritid_first'], form_list=form_list)
            vosoritid_first = vosoritid_first_form.save(commit=False)
            vosoritid_first.profile = child_addition
            vosoritid_first.save()

        # Step 5: Save the rehabilitation record if applicable
        if child_profile_form.cleaned_data.get('rehabilitation'):
            rehab_record_form = get_my_form(list_of_forms['rehab_record'], form_list=form_list)
            rehab_record = rehab_record_form.save(commit=False)
            rehab_record.profile = child_profile
            rehab_record.save()

        return redirect('user:login')

    def skip_rehabilitation_record(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('childprofile') or {}
        return cleaned_data.get('rehabilitation', True)

    def skip_vosoritid(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('childprofile') or {}
        return cleaned_data.get('vosoritid', True)

    condition_dict = {
        'rehab_record': skip_rehabilitation_record,
        'vosoritid_first': skip_vosoritid,
    }

class DoctorRegisterView(View):
    def get(self, request):
        user_form = DoctorCreationForm()
        profile_form = DoctorProfileForm()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'global_title': _('Регистрация врача')
        }
        return render(request, 'user/register_page.html', context)

    def post(self, request):
        user_form = DoctorCreationForm(request.POST)
        profile_form = DoctorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('user:login')
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'global_title': _('Регистрация врача')
        }
        return render(request, 'user/register_page.html', context)


class ProfileView(CustomLoginRequiredMixin, View):
    def get(self, request):
        speciality = None
        if request.user.is_doctor:
            user_form = DoctorUserEditForm(instance=request.user)
            speciality = request.user.doctorprofile.speciality
            profile_form = None
            additional_info = None
        elif request.user.is_patient:
            if request.user.patient_altprofile.is_child:
                user_form = PatientChildUserEditForm(instance=request.user)
                profile_form = PatientChildProfileEditForm(instance=request.user.patient_altprofile)
                additional_info = ChildAdditionUpdateForm(instance=request.user.patient_altprofile.ChildAddition)
            else:
                user_form = PatientUserEditForm(instance=request.user)
                profile_form = PatientProfileEditForm(instance=request.user.patient_altprofile)
                additional_info = None
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = None
            additional_info = None
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'additional_info': additional_info,
            'speciality': speciality
        }
        return render(request, 'user/profile.html', context)

    def post(self, request):
        speciality = None
        if request.user.is_doctor:
            user_form = DoctorUserEditForm(request.POST, instance=request.user)
            speciality = request.user.doctorprofile.speciality
            profile_form = None
            additional_info = None
            if user_form.is_valid():
                user_form.save()
        elif request.user.is_patient:
            if request.user.patient_altprofile.is_child:
                user_form = PatientChildUserEditForm(request.POST, instance=request.user)
                profile_form = PatientChildProfileEditForm(request.POST, instance=request.user.patient_altprofile)
                additional_info = ChildAdditionUpdateForm(request.POST,
                                                          instance=request.user.patient_altprofile.ChildAddition)
                if user_form.is_valid() and profile_form.is_valid() and additional_info.is_valid():
                    user_form.save()
                    profile_form.save()
                    additional_info.save()
            else:
                user_form = PatientUserEditForm(request.POST, instance=request.user)
                profile_form = PatientProfileEditForm(request.POST, instance=request.user.patient_altprofile)
                additional_info = None
                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    profile_form.save()
        else:
            user_form = UserEditForm(request.POST, instance=request.user)
            profile_form = None
            additional_info = None
            if user_form.is_valid():
                user_form.save()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'additional_info': additional_info,
            'speciality': speciality
        }
        return render(request, 'user/profile.html', context)


def patient_search_view(request):
    form = PatientSearchForm(request.GET or None)
    patients = []

    if request.GET and form.is_valid():
        patients = form.search()

    context = {
        'form': form,
        'patients': patients,
    }
    return render(request, 'user/patients.html', context)


def patient_detail(request, pk):
    patient = get_object_or_404(PatientAltProfile, pk=pk)

    # Для ребенка пациента
    if patient.is_child:
        vosoritid_first_record = VosoritidFirstRecord.objects.filter(user=patient.ChildAddition).first()
        vosoritid_second_record = VosoritidRecord.objects.filter(user=patient.ChildAddition)
        rehabilitation_records = RehabilitationRecord.objects.filter(profile=patient)
        doctor_checks = DoctorCheck.objects.filter(profile=patient.ChildAddition)
        vosoritid = True if vosoritid_first_record else False
        context = {
            'patient': patient,
            'vosoritid_first_record': vosoritid_first_record,
            'vosoritid_second_record': vosoritid_second_record,
            'rehabilitation_records': rehabilitation_records,
            'doctor_checks': doctor_checks,
            'vosoritid': vosoritid,
        }
    # Для взрослого пациента
    else:
        vosoritid_period = VosoritidPeriod.objects.filter(profile=patient.AdultAddition).first()
        rehabilitation_records = RehabilitationRecord.objects.filter(profile=patient)
        vosoritid = True if vosoritid_period else False
        context = {
            'patient': patient,
            'vosoritid_period': vosoritid_period,
            'rehabilitation_records': rehabilitation_records,
            'vosoritid': vosoritid,
        }

    return render(request, 'user/patient_profile.html', context)
