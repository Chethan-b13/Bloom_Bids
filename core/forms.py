import email
from logging import PlaceHolder
from django import forms
from .models import UserAddress
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class AddressForm(forms.ModelForm):
    """Form definition for Address."""

    country = CountryField(blank_label='Select Your Country').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'style': 'text-align: center;padding: 1.2rem; color: #666; background: #f8e3e8;',

    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'yourname@mail.com',
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'room - street - locality'
    }))

    class Meta:
        """Meta definition for Addressform."""

        model = UserAddress
        fields = ('name', 'email', 'address',
                  'city', 'state', 'zip', 'country')
