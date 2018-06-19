#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class GtokenForm(forms.Form):
    gtoken_code = forms.CharField(max_length=100, label=_("Google Authenticator Code"), required=True)
    
class SubmitGtokenForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    gtoken_code = forms.CharField(max_length=100, required=True)
    auth_token = forms.CharField(max_length=100, required=True)
    gtoken = forms.CharField(max_length=100, required=True)
    uuid = forms.CharField(max_length=100, required=True)
