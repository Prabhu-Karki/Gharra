from django import forms
from .models import Customer
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import  PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model= Customer
        fields= ['name', 'locality', 'city', 'state',  'email', 'phone']
        widgets= {'name':forms.TextInput(attrs={'class': 'form-control'}),'locality':forms.TextInput(attrs={'class': 'form-control'}),'city':forms.TextInput(attrs={'class': 'form-control'}), 'state':forms.Select(attrs={'class': 'form-control'}), 'phone':forms.NumberInput(attrs={'class': 'form-control'}), 'email':forms.EmailInput(attrs={'class': 'form-control'})}

class MyPasswordChangeForms(PasswordChangeForm):
    old_password= forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'form-control'}))
    new_password1= forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())


class MyPasswordResetForm(PasswordResetForm):
    email= forms.EmailField(label=_('Email'), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label= _('New password'), widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}), strip=False, help_text=password_validation.password_validators_help_text_html(),)
    new_password2 = forms.CharField(label=_("New password confirmation"), strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),)
