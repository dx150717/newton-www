# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)
    password = forms.CharField(widget=forms.PasswordInput(),label=_("Password"), required=True)

class GoogleAuthenticatorForm(forms.Form):
    gtoken_code = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(label=_("Email"), required=True)
    password = forms.CharField(widget=forms.PasswordInput(),label=_("Password"), required=True)
    auth_token = forms.CharField(required=True, max_length=100)