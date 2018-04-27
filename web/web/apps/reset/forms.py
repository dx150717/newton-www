# -*- coding: utf-8 -*-
from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField()

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    repassword = forms.CharField(widget=forms.PasswordInput())



