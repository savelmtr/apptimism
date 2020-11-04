from django_registration import validators
from django.utils.translation import gettext, gettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from users.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm


User = get_user_model()


class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs = {
            'class': 'form-control', 'placeholder': self.fields['old_password'].label}
        self.fields['old_password'].label = False
        self.fields['new_password1'].widget.attrs = {
            'class': 'form-control', 'placeholder': self.fields['new_password1'].label}
        self.fields['new_password1'].label = False
        self.fields['new_password2'].widget.attrs = {'class': 'form-control', 'placeholder': self.fields['new_password2'].label}
        self.fields['new_password2'].label = False


class ResetPasswordForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = False
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': _("Email")}


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': _("Email")}
        self.fields['password'].label = False
        self.fields['password'].widget.attrs={'class': 'form-control', 'placeholder': _("Password")}



class CustomRegistrationForm(CustomUserCreationForm):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should take care when overriding ``save()`` to respect
    the ``commit=False`` argument, as several registration workflows
    will make use of it to create inactive user accounts.

    """

    class Meta(CustomUserCreationForm.Meta):
        fields = [
            User.get_email_field_name(),
            "first_name",
            "lang",
            "password1",
            "password2",
        ]

    error_css_class = "error"
    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        email_field = User.get_email_field_name()

        self.fields[email_field].label = False
        self.fields[email_field].max_length=254
        self.fields[email_field].widget=forms.EmailInput(
            attrs={'class': 'form-control', 'autofocus': True, 'placeholder': _("Email")})
        self.fields[email_field].validators.extend(
            (validators.HTML5EmailValidator(), validators.validate_confusables_email)
        )
        self.fields[email_field].required = True
        self.fields['first_name'].required=True
        self.fields['first_name'].label=False
        self.fields['first_name'].widget.attrs={
            'class': 'form-control', 'placeholder': _("First name")}
        self.fields['lang'].required=True
        self.fields['lang'].widget.attrs={'class': 'form-control'}
        self.fields['password1'].label = False
        self.fields['password1'].widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': _("Password")})
        self.fields['password2'].label = False
        self.fields['password2'].widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': _("Password confirmation")})