#-*- coding: utf-8 -*-
""" forms of register.
    1. EmailForm for register index.
    2. PasswordForm for set password.
    3. GtokenForm for set google authenticator
"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from utils import validators

class EmailForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Password"), required=True, min_length=6, max_length=16, validators=[validators.valid_password])
    repassword = forms.CharField(widget=forms.PasswordInput(), label=_("Confirm Password"), required=True, min_length=6, max_length=16, validators=[validators.valid_password])

class GtokenForm(forms.Form):
    gtoken_code = forms.CharField(max_length=100, label=_("Google Authenticator Code"), required=True)
    
class SubmitGtokenForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    gtoken_code = forms.CharField(max_length=100, required=True)
    auth_token = forms.CharField(max_length=100, required=True)
    gtoken = forms.CharField(max_length=100, required=True)
    uuid = forms.CharField(max_length=100, required=True)
