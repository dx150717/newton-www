# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from tokenexchange import models as tokenexchange_models
from user import forms as user_forms

class KYCInfoForm(ModelForm):
    cellphone_group = user_forms.CellphoneGroupField(label=_('cellphone'),required=True, widget=user_forms.CellphoneGroupWidget)
    def __init__(self, *args, **kw):
        super(KYCInfoForm, self).__init__(*args, **kw)
        self.fields.keyOrder = ['first_name',
                                'last_name',
                                'id_number',
                                'id_card',
                                'cellphone_group',
                                'location',
                                'how_to_contribute',
                                'what_is_newton',
        ]

    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'first_name',
            'last_name',
            'location',
            'id_number',
            'id_card',
            'how_to_contribute',
            'what_is_newton',
        ]

class ApplyAmountForm(ModelForm):
    class Meta:
        model = tokenexchange_models.InvestInvite
        fields = [
            'expect_btc',
            'expect_ela',
        ]

class AcceptDistributionForm(forms.Form):
    accept_btc = forms.FloatField(label=_('Amount of BTC'), required=True, widget=forms.NumberInput(attrs={'step':0.01}))
    accept_ela = forms.FloatField(label=_('Amount of ELA'), required=True, widget=forms.NumberInput(attrs={'step':1}))
