import json

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from formtools.wizard.views import SessionWizardView
from .forms import (
    LoginForm,
    PatientRegistrationForm,
    CombinedAdultProfileForm
)
from medicine.forms import ElongationRecordForm, VosoritidPeriodRecordForm, RehabilitationRecordForm


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
        return context

    def get_exact_form(formlist, name):
        for form_name, form_item, *z in formlist.form_list:
            print("123 {0}".format(form_item))
            print(form_name)
            if form_name == name:
                print("123 {0}".format(form_item))
                print(form_name)
                return form_item


    def done(self, form_list, **kwargs):
        forms = {form.prefix: form for form in form_list}
        if 'patient' in forms:
            patient = forms['patient'].save()
            profile = forms['adultprofile'].save(commit=False)
            profile.user = patient
            profile.save()
            adult_addition = CombinedAdultProfileForm.get_additional_data(patient.pk)
            if 'elongation' in forms and forms['elongation'].has_changed():
                elongation = forms['elongation'].save(commit=False)
                elongation.profile = adult_addition
                elongation.save()
        # patient_form = self.get_exact_form(name='patient')
        # patient_form.save(commit=False)

        # patient = patient_form.save()
        # adultprofile_form = form_list[1]
        # adultprofile= adultprofile_form.save(commit=False)
        # adultprofile.user = patient
        # adultprofile.save()
        #print(adultprofile)
        return HttpResponse("123")

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

def test(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        form2 = CombinedAdultProfileForm(data=request.POST)
        if form.is_valid() and form2.is_valid():
            #form2.save()
            return redirect('pages:index')  # Замените 'success_url' на реальный URL
    else:
        form = PatientRegistrationForm()
        form2 = CombinedAdultProfileForm()
    return render(request, 'user/test.html', {'form': form, 'form2': form2})

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

