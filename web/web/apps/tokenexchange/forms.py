# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from tokenexchange import models as tokenexchange_models

class KYCInfoForm(ModelForm):
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'first_name',
            'last_name',
            'id_card',
            'expect_btc',
            'expect_ela',
            'how_to_contribute',
            'what_is_newton',
        ]

class KYCAddressForm(ModelForm):
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'max_btc_limit',
            'max_ela_limit',
            'receive_btc_address',
            'receive_ela_address',
        ]
