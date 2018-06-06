# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class SubscribeForm(forms.Form):
    email_address = forms.EmailField(label=_("Email"), required=True)