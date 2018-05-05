# -*- coding: utf-8 -*-
from django import forms

class ConfirmKYCForm(forms.Form):
    level = forms.IntegerField(required=True)
    user_id = forms.IntegerField(required=True)
    pass_kyc = forms.IntegerField(required=True)

class AmountForm(forms.Form):
    user_id = forms.IntegerField(required=True)
    assign_btc = forms.FloatField(required=True)
    assign_ela = forms.FloatField(required=True)

class PostInviteForm(forms.Form):
    user_id = forms.IntegerField(required=True)
