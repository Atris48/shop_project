from account_app.models import User
from django import forms

from profile_app.models import Address


class UserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'fullname', 'email', 'national_code', ]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['birthdate', ]


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', ]
