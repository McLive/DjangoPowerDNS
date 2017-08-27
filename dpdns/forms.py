from django import forms
from django.forms import ModelForm

from dpdns.models import Domains, DomainAccess


class LoginForm(forms.Form):
    username = forms.CharField(max_length=18)
    password = forms.CharField(widget=forms.PasswordInput())


class DomainAddForm(ModelForm):
    class Meta:
        model = Domains
        fields = ['name']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'The name of your Domain.'
                }),
        }


class DomainUserAddForm(ModelForm):
    class Meta:
        model = DomainAccess
        fields = ['user']

        """widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'The name of your Domain.'
                }),
        }"""
