# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)
    password = forms.CharField(widget=forms.PasswordInput(),label=_("Password"), required=True)
    code = forms.CharField(required=True, label=_("Verification Code"))
    code.widget.attrs.update({"autocomplete":"off"})