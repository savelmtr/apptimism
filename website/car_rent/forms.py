from django.forms import ModelForm

from .models import Car


class CarEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_ru'].widget.attrs = {
            'class': 'form-control', 'placeholder': self.fields['name_ru'].label, 'required': True}
        self.fields['name_ru'].label = False
        self.fields['name_en'].widget.attrs = {
            'class': 'form-control', 'placeholder': self.fields['name_en'].label}
        self.fields['name_en'].label = False
        self.fields['production_year'].widget.attrs = {
            'class': 'form-control', 'placeholder': self.fields['production_year'].label}
        self.fields['production_year'].label = False

    class Meta:
        model = Car
        exclude = ('created_at', 'renter')
