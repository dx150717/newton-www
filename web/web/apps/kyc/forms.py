# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from kyc import models as kyc_models

class KYCInfoForm(ModelForm):
    class Meta:
        model = kyc_models.KYCInfo
        fields = [
            'first_name',
            'last_name',
            'id_card',
            'expect_btc',
            'expect_ela',
            'how_to_contribute',
            'what_is_newton',
            'btc_address',
            'ela_address',
        ]

