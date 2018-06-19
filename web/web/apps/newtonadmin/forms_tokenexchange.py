# -*- coding: utf-8 -*-
from django import forms
from django_countries.fields import CountryField

from config import codes

class ConfirmKYCForm(forms.Form):
    level = forms.IntegerField(required=True)
    user_id = forms.IntegerField(required=True)
    pass_kyc = forms.IntegerField(required=True)
    comment = forms.CharField(max_length=1000)

class AmountForm(forms.Form):
    user_id = forms.IntegerField(required=True)
    assign_btc = forms.FloatField(required=True)
    assign_ela = forms.FloatField(required=True)

class PostInviteForm(forms.Form):
    user_id = forms.IntegerField(required=True)

class KYCQueryForm(forms.Form):
    KYC_TYPE_OPTIONS = (
        (codes.KYCType.INDIVIDUAL.value, codes.KYCType.INDIVIDUAL.name),
        (codes.KYCType.ORGANIZATION.value, codes.KYCType.ORGANIZATION.name),
    )
    NODE_OPTIONS = (
        (1, 'yes'),
        (0, 'no'),
    )
    kyc_type = forms.ChoiceField(widget=forms.Select, choices=KYC_TYPE_OPTIONS)
    is_establish_node = forms.ChoiceField(widget=forms.Select, choices=NODE_OPTIONS)
    country = CountryField()

