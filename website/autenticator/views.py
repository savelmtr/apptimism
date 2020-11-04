from django.contrib.auth.views import (LoginView, PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django_registration.backends.activation.views import (ActivationView,
                                                           RegistrationView)

from .forms import CustomRegistrationForm, LoginForm, ResetPasswordForm, ChangePasswordForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginPage(LoginView):

    form_class = LoginForm

    template_name = 'auth/login.html'


class RegistrationPage(RegistrationView):

    template_name = 'auth/registration_form.html'
    
    email_body_template = 'auth/activation_email_body.txt'

    email_subject_template = 'auth/activation_email_subject.txt'
    
    form_class = CustomRegistrationForm
    
    success_url = reverse_lazy('auth:registration_complete')


class RegistrationComplete(TemplateView):

    template_name = 'auth/registration_complete.html'


class ActivationPage(ActivationView):
    
    template_name = 'auth/activation_failed.html'

    success_url = reverse_lazy('auth:activation_complete')


class ActivationComplete(TemplateView):

    template_name = 'auth/activation_complete.html'


@method_decorator(login_required, name='dispatch')
class PasswordChangePage(PasswordChangeView):
    
    template_name = 'auth/password_change_form.html'

    success_url = reverse_lazy('auth:password_change_done')

    form_class = ChangePasswordForm


@method_decorator(login_required, name='dispatch')
class PasswordChangeDonePage(PasswordChangeDoneView):

    template_name = 'auth/password_change_done.html'


class PasswordResetPage(PasswordResetView):
    
    subject_template_name = 'auth/password_reset_subject.txt'
    
    email_template_name = 'auth/password_reset_email.html'
    
    template_name = 'auth/password_reset_form.html'

    form_class = ResetPasswordForm

    success_url = reverse_lazy('auth:password_reset_done')


class PasswordResetDonePage(PasswordResetDoneView):
    
    template_name = 'auth/password_reset_done.html'


class PasswordResetConfirmPage(PasswordResetConfirmView):
    
    template_name = 'auth/password_reset_confirm.html'
    
    #form_class=MySetPasswordForm,
    
    success_url = reverse_lazy('auth:password_reset_complete')


class PasswordResetCompletePage(PasswordResetCompleteView):

    template_name = 'auth/password_reset_complete.html'
