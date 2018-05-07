# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from tokenexchange import models as tokenexchange_models
from user import forms as user_forms

class KYCInfoForm(ModelForm):
    cellphone_group = user_forms.CellphoneGroupField(required=True, widget=user_forms.CellphoneGroupWidget, label=_("Cellphone"))
    cellphone_of_emergency_contact = user_forms.CellphoneGroupField(required=True, widget=user_forms.CellphoneGroupWidget, label=_("Emergency Cellphone"))
    def __init__(self, *args, **kw):
        super(KYCInfoForm, self).__init__(*args, **kw)
        self.fields.keyOrder = ['first_name',
                                'last_name',
                                'country',
                                'id_number',
                                'id_card',
                                'cellphone_group',
                                'location',
                                'how_to_contribute',
                                'what_is_newton',
                                'emergency_contact_first_name',
                                'emergency_contact_last_name',
                                'cellphone_of_emergency_contact',
        ]

    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'first_name',
            'last_name',
            'country',
            'location',
            'id_number',
            'id_card',
            'how_to_contribute',
            'what_is_newton',
            'emergency_contact_first_name',
            'emergency_contact_last_name',
            'cellphone_of_emergency_contact',
        ]

class ApplyAmountForm(ModelForm):
    class Meta:
        model = tokenexchange_models.InvestInvite
        fields = [
            'expect_btc',
            'expect_ela',
        ]
