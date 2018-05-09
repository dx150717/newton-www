# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput(),label=_("Password"))



