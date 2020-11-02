from django.contrib.auth.views import (LoginView, PasswordChangeView, 
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView)

from django.views.generic.base import TemplateView

#from .forms import AuthenticationFormWithCaptcha, RegistrationFormWithCaptcha, PasswordChangeFormWithCaptcha
from django.conf import settings
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django.urls import reverse_lazy


class LoginPage(LoginView):

    #form_class = AuthenticationFormWithCaptcha

    template_name = 'auth/login.html'


class RegistrationPage(RegistrationView):

    template_name = 'auth/registration_form.html'
    
    email_body_template = 'auth/activation_email_body.txt'

    email_subject_template = 'auth/activation_email_subject.txt'
    
    #form_class = RegistrationFormWithCaptcha
    
    success_url = reverse_lazy('auth:registration_complete')


class RegistrationComplete(TemlateView):

    template_name = 'auth/registration_complete.html'


class ActivationPage(ActivationView):
    
    template_name = 'auth/activation_failed.html'

    success_url = reverse_lazy('auth:activation_complete')


class ActivateComplete(TemlateView):

    template_name = 'auth/activation_complete.html'


class PasswordChangePage(PasswordChangeView):
    
    template_name = 'auth/password_change_form.html'

    success_url = reverse_lazy('auth:password_change_done')

    #form_class = PasswordChangeFormWithCaptcha


class PasswordChangeDonePage(PasswordChangeDoneView):

    template_name = 'auth/password_change_done.html'


class PasswordResetPage(PasswordResetView):
    
    subject_template_name = 'auth/password_reset_subject.txt'
    
    email_template_name = 'auth/password_reset_email.html'
    
    template_name = 'auth/password_reset_form.html'

    #form_class = MyPasswordResetForm

    success_url = reverse_lazy('auth:password_reset_done')


class PasswordResetDonePage(PasswordResetDoneView):
    
    template_name = 'auth/password_reset_done.html'


class PasswordResetConfirmPage(PasswordResetConfirmView):
    
    template_name = 'auth/password_reset_confirm.html'
    
    #form_class=MySetPasswordForm,
    
    success_url = reverse_lazy('auth:password_reset_complete')


class PasswordResetCompletePage(PasswordResetCompleteView):

    template_name = 'auth/password_reset_complete.html'