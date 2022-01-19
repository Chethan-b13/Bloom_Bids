import email
from logging import PlaceHolder
from unittest.util import _MAX_LENGTH
from django import forms
from .models import UserAddress
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class AddressForm(forms.ModelForm):
    """Form definition for Address."""

    # country = CountryField(blank_label='Select Your Country').formfield(widget=CountrySelectWidget(attrs={
    #     'class': 'custom-select d-block w-100',
    #     'style': 'text-align: center;padding: 1.2rem; color: #666; background: #f8e3e8;',

    # }))

    Card_no = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1111-2222-3333-4444',
    }))
    Name_on_card = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })),
    # cvv = forms.IntegerField(max_value=999, widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': '123',
    # })),

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
                  'city', 'state', 'zip', 'Name_on_card', 'Card_no', 'cvv', 'exp_month', 'exp_year')
