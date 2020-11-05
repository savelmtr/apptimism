from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_registration import validators

from django.forms import ModelForm

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

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', )
