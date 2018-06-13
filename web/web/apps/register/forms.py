#-*- coding: utf-8 -*-
""" forms of register.
    1. EmailForm for register index.
    2. PasswordForm for set password.
    3. GtokenForm for set google authenticator
"""
from django import forms
from django.utils.translation import ugettext_lazy as _


class EmailForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)
    code = forms.CharField(required=True, label=_("Verification Code"))
    code.widget.attrs.update({"autocomplete":"off"})

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Password"), required=True)
    repassword = forms.CharField(widget=forms.PasswordInput(), label=_("Confirm Password"), required=True)

class GtokenForm(forms.Form):
    gtoken_code = forms.CharField(max_length=100, label=_("Google Authenticator Code"), required=True)
    

