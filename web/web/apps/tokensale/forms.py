# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from tokensale import models as tokensale_models

class KYCInfoForm(ModelForm):
    class Meta:
        model = tokensale_models.KYCInfo
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

