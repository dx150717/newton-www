# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from tokenexchange import models as tokenexchange_models

class KYCInfoForm(ModelForm):
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'first_name',
            'last_name',
            'id_card',
            'how_to_contribute',
            'what_is_newton',
        ]

class ApplyAmountForm(ModelForm):
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'expect_btc',
            'expect_ela',
        ]

class AcceptDistributionForm(forms.Form):
    accept_btc = forms.FloatField(label=_('Amount of BTC'), required=True, widget=forms.NumberInput(attrs={'step':0.01}))
    accept_ela = forms.FloatField(label=_('Amount of ELA'), required=True, widget=forms.NumberInput(attrs={'step':1}))
