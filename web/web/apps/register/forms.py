# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _


class EmailForm(forms.Form):
    email = forms.EmailField()

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    repassword = forms.CharField(widget=forms.PasswordInput())


