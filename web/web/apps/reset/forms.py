# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from utils import validators

class EmailForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Password"), required=True, min_length=6, max_length=16, validators=[validators.valid_password])
    repassword = forms.CharField(widget=forms.PasswordInput(), label=_("Repassword"), required=True, min_length=6, max_length=16, validators=[validators.valid_password])