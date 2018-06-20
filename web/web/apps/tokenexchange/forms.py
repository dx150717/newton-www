# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from tokenexchange import models as tokenexchange_models
from user import forms as user_forms

'''
'''

class KYCBaseForm(ModelForm):
    """advanceinfo for kyc example: what can you do for newton
    """
    cellphone_group = user_forms.CellphoneGroupField(required=True, widget=user_forms.CellphoneGroupWidget, label=_("Cellphone"), help_text='(*)')
    def __init__(self, *args, **kw):
        super(KYCBaseForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'id_type',
            'id_number',
            'id_card',
            'country',
            'city',
            'location',
            'cellphone_group',
        ]

    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'first_name',
            'last_name',
            'country',
            'city',
            'location',
            'id_type',
            'id_number',
            'id_card'
        ]

class OrganizationBaseForm(ModelForm):
    """advanceinfo for kyc example: what can you do for newton
    """
    cellphone_group = user_forms.CellphoneGroupField(required=True, widget=user_forms.CellphoneGroupWidget, label=_("Cellphone"), help_text='(*)')
    def __init__(self, *args, **kw):
        super(OrganizationBaseForm, self).__init__(*args, **kw)
        self.fields['country'].label = _('Registration Country')
        self.fields['orgnization_certificate2'].required = False
        self.fields.keyOrder = [
            'orgnization_name',
            'orgnization_code',
            'orgnization_certificate1',
            'orgnization_certificate2',
            'country',
            'first_name',
            'last_name',
            'cellphone_group',
        ]

    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'orgnization_name',
            'orgnization_code',
            'orgnization_certificate1',
            'orgnization_certificate2',
            'country',
            'first_name',
            'last_name',
            'cellphone_group',
        ]

class KYCProfileForm(ModelForm):
    """ kyc profile """
    def __init__(self, *args, **kw):
        super(KYCProfileForm, self).__init__(*args, **kw)
        self.fields['facebook'].required = False
        self.fields['twitter'].required = False
        self.fields['telegram'].required = False
        self.fields['wechat'].required = False
        self.fields['other_social_account'].required = False
        self.fields['personal_profile_attachment'].required = False
        self.fields['your_community'].required = False
        self.fields['your_community_screenshots1'].required = False
        self.fields['your_community_screenshots2'].required = False
        self.fields['your_community_screenshots3'].required = False
        self.fields.keyOrder = [
            'personal_profile',
            'personal_profile_attachment',
            'wechat',
            'telegram',
            'twitter',
            'facebook',
            'other_social_account',
            'your_community',
            'your_community_screenshots1',
            'your_community_screenshots2',
            'your_community_screenshots3',
        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'personal_profile',
            'personal_profile_attachment',
            'wechat',
            'telegram',
            'twitter',
            'facebook',
            'other_social_account',
            'your_community',
            'your_community_screenshots1',
            'your_community_screenshots2',
            'your_community_screenshots3',
        ]

class OrganizationProfileForm(ModelForm):
    """ kyc profile """
    def __init__(self, *args, **kw):
        super(OrganizationProfileForm, self).__init__(*args, **kw)
        self.fields['wechat_platform_name'].required = False
        self.fields['twitter'].required = False
        self.fields['facebook'].required = False
        self.fields['other_social_account'].required = False
        self.fields['personal_profile_attachment'].required = False
        self.fields['personal_profile'].label = _("Organization Introduction")

        self.fields.keyOrder = [
            'personal_profile',
            'personal_profile_attachment',
            'wechat_platform_name',
            'twitter',
            'facebook',
            'other_social_account',
        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'personal_profile',
            'personal_profile_attachment',
            'wechat_platform_name',
            'twitter',
            'facebook',
            'other_social_account',
        ]
        

class ContributeForm(ModelForm):
    """how to contribut for newton form"""
    def __init__(self, *args, **kw):
        super(ContributeForm, self).__init__(*args, **kw)
        self.fields['done_for_newton'].required = False
        self.fields['done_for_newton_attachment'].required = False
        self.fields['do_for_newton'].required = False
        self.fields.keyOrder = [
            'what_is_newton',
            'done_for_newton',
            'done_for_newton_attachment',
            'do_for_newton'

        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'what_is_newton',
            'done_for_newton',
            'done_for_newton_attachment',
            'do_for_newton'
        ]

class EmergencyForm(ModelForm):
    """docstring for EmergencyForm"""
    cellphone_of_emergency_contact = user_forms.CellphoneGroupField(required=True, widget=user_forms.CellphoneGroupWidget, label=_('Cellphone'), help_text='(*)')
    def __init__(self, *args, **kw):
        super(EmergencyForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'emergency_contact_first_name',
            'emergency_contact_last_name',
            'cellphone_of_emergency_contact',
            'emergency_country',
            'emergency_city',
            'emergency_location',
            'emergency_relationship',
        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'emergency_contact_first_name',
            'emergency_contact_last_name',
            'emergency_country',
            'emergency_city',
            'emergency_location',
            'emergency_relationship'
        ]

class ApplyAmountForm(ModelForm):
    class Meta:
        model = tokenexchange_models.InvestInvite
        fields = [
            'expect_btc',
            'expect_ela',
        ]

class CountryForm(ModelForm):
    def __init__(self, *args, **kw):
        super(CountryForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'country',
        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'country',
        ]

class OrganizationCountryForm(ModelForm):
    def __init__(self, *args, **kw):
        super(OrganizationCountryForm, self).__init__(*args, **kw)
        self.fields['country'].label = _("Registration Country")
        self.fields.keyOrder = [
            'country',
        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'country',
        ]

class EmergencyCountryForm(ModelForm):
    def __init__(self, *args, **kw):
        super(EmergencyCountryForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'emergency_country',
        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'emergency_country',
        ]