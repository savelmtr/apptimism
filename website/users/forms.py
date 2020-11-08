from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm
from django_registration import validators

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class UserEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].validators.extend(
            (validators.HTML5EmailValidator(), validators.validate_confusables_email)
        )
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control', 'placeholder': self.fields['first_name'].label, 'required': True}
        self.fields['first_name'].label = False
        self.fields['email'].widget.attrs = {
            'class': 'form-control', 'placeholder': self.fields['email'].label}
        self.fields['email'].label = False

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', )
