from django import forms

from django.contrib.auth.models import User

from users.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',)
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'location', 'additional_info')

        help_texts = {'phone_number': ''}
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'initial': '+380',
                'maxlength': '20',
                'required': True
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'initial': '',
                'maxlength': '100',
                'required': True

            }),
            'additional_info': forms.TextInput(attrs={
                'class': 'form-control',
                'initial': '',
            }),
        }





