import json

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from formtools.wizard.views import SessionWizardView

from medicine.models import Elongation, VosoritidPeriod, RehabilitationRecord
from .forms import (
    LoginForm,
    PatientRegistrationForm,
    CombinedAdultProfileForm
)
from medicine.forms import ElongationRecordForm, VosoritidPeriodRecordForm, RehabilitationRecordForm
from .models import Patient, AdultProfile, AdultAddition


def index(request):
    return render(request, 'user/index.html')

def user_login(request):
    if not request.user.is_authenticated:
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
                        return redirect('pages:index')
                    else:
                        return HttpResponse('Disabled account')
            else:
                context = {'form': form}
                return render(request, 'user/login.html', context)
        else:
            form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    else:
        return redirect('pages:index')

def user_logout(request):
    user_logout(request)
    return redirect('pages:index')

def return_forms(request, patient_type):
    context = {'title': 'Регистрация'}
    # if patient_type == 'patient':
    #     context['form'] = PatientCreationForm(request.POST or None)
    #     context['form2'] = PatientProfileForm(request.POST or None)
    #     return render(request, 'user/register.html', context)
    # elif patient_type == 'parents':
    #     context['form'] = PatientChildCreationForm(request.POST or None)
    #     context['form2'] = PatientChildProfileForm(request.POST or None)
    #     return render(request, 'user/register.html', context)
    # elif patient_type == 'doctor':
    #     context['form'] = DoctorCreationForm(request.POST or None)
    #     context['form2'] = DoctorProfileForm(request.POST or None)
    #     return render(request, 'user/register.html', context)
    # else:
    #     return redirect('index')

def forms_valid_or_not(request, form, form2, context):
    print('2')
    if form.is_valid() and form2.is_valid():
        parent = form.save(commit=True)
        child = form2.save(commit=False)
        child.user = parent
        child.save()
        print('here')
        return redirect('user_login')
    else:
        context['form'] = form
        context['form2'] = form2
        return render(request, 'user/register.html', context)

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
}

class TestWizard(SessionWizardView):
    template_name = 'user/test.html'
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
        self.get_form_list()
        return context


    def done(self, form_list, **kwargs):
        # print(form_list)
        # Step 1: Save the patient
        patient_form = form_list[0]
        patient = patient_form.save()
        #test = self.get_cleaned_data_for_step('')

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

        return HttpResponse("All data has been saved successfully.")

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



def user_register(request, patient_type):
    context = {'title': 'Регистрация'}
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        form2 = CombinedAdultProfileForm(request.POST)
        if form.is_valid() and form2.is_valid():
            parent = form.save(commit=True)
            child = form2.save(commit=False)
            child.user = parent
            child.save()
            print('here')
            return redirect('user_login')
        else:
            context['form'] = form
            context['form2'] = form2
            return render(request, 'user/register.html', context)
    else:
        form = PatientRegistrationForm(request.POST or None)
        form2 = CombinedAdultProfileForm(request.POST or None)
        context['form'] = form
        context['form2'] = form2
        return render(request, 'user/register.html', context)

    # if request.method == 'POST':
    #     if patient_type == 'patient':
    #         form = PatientCreationForm(request.POST)
    #         form2 = PatientProfileForm(request.POST)
    #         print('1')
    #         return forms_valid_or_not(request, form, form2, context)
    #     elif patient_type == 'parents':
    #         form = PatientChildCreationForm(request.POST)
    #         form2 = PatientChildProfileForm(request.POST)
    #         return forms_valid_or_not(request, form, form2, context)
    #     elif patient_type == 'doctor':
    #         form = DoctorCreationForm(request.POST)
    #         form2 = DoctorProfileForm(request.POST)
    #         return forms_valid_or_not(request, form, form2, context)
    # else:
    #     return return_forms(request, patient_type)

