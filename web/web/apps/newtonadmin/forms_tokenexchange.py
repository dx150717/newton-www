# -*- coding: utf-8 -*-
from django import forms

class ConfirmKYCForm(forms.Form):
    level = forms.IntegerField(required=True)
    user_id = forms.IntegerField(required=True)
    pass_kyc = forms.IntegerField(required=True)

class AmountForm(forms.Form):
    user_id = forms.IntegerField(required=True)
    min_btc_limit = forms.FloatField(required=True)
    max_btc_limit = forms.FloatField(required=True)
    min_ela_limit = forms.FloatField(required=True)
    max_ela_limit = forms.FloatField(required=True)

class PostInviteForm(forms.Form):
    user_id = forms.IntegerField(required=True)
