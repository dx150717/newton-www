# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class EmailForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Password"), required=True)
    repassword = forms.CharField(widget=forms.PasswordInput(), label=_("Repassword"), required=True)



