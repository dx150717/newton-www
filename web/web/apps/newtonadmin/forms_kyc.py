# -*- coding: utf-8 -*-
from django import forms

class IDConfirmForm(forms.Form):
    pass_kyc = forms.IntegerField()
