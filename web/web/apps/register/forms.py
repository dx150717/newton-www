# -*- coding: utf-8 -*-
from django import forms

class EmailForm(forms.Form):
    email = forms.PasswordInput()

class PasswordForm(forms.Form):
    password = forms.PasswordInput()

