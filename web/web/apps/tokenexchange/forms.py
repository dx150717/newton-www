# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from tokenexchange import models as tokenexchange_models
from user import forms as user_forms

'''
first_name = models.CharField(max_length=128, verbose_name='First Name', required=True)
last_name = models.CharField(max_length=128, verbose_name='Last Name', required=True)
country_code = models.CharField(max_length=4, db_index=True, required=True)            
cellphone = models.CharField(max_length=20, db_index=True, required=True)
country = CountryField(blank_label="Select country or region", verbose_name='Country or Region', required=True)
state = models.CharField(max_length=256, verbose_name='State', required=True)
location = models.CharField(max_length=1024, verbose_name='Location', required=True)
id_type = models.IntegerField(
    _('id_type'),
    choices=ID_CHOICES, default=codes.IDType.ID_CARD.value,
    db_index=True,
    required=True
)
id_number = models.CharField(max_length=128, db_index=True, verbose_name='ID Number', required=True)
id_card = models.FileField(required=True, upload_to=storage.hashfile_upload_to('id_card', path_prefix='id_card'), verbose_name='ID Photo', validators=[validators.validate_file_extension_of_id_photo, validators.validate_file_size_of_id_photo])
'''

class KYCBaseForm(ModelForm):
    """advanceinfo for kyc example: what can you do for newton
    """
    cellphone_group = user_forms.CellphoneGroupField(required=True, widget=user_forms.CellphoneGroupWidget, label="Cellphone")
    def __init__(self, *args, **kw):
        super(KYCBaseForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'cellphone_group',
            'country',
            'city',
            'location',
            'id_type',
            'id_number',
            'id_card'
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


class KYCProfileForm(ModelForm):
    """ kyc profile """
    def __init__(self, *args, **kw):
        super(KYCProfileForm, self).__init__(*args, **kw)
        self.fields['personal_profile'].required = False
        self.fields['personal_profile_attachment'].required = False
        self.fields['facebook'].required = False
        self.fields['twitter'].required = False
        self.fields['telegram'].required = False
        self.fields['wechat'].required = False
        self.fields['other_social_account'].required = False

        self.fields.keyOrder = [
            'personal_profile',
            'personal_profile_attachment',
            'facebook',
            'twitter',
            'telegram',
            'wechat',
            'other_social_account'
        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'personal_profile',
            'personal_profile_attachment',
            'facebook',
            'twitter',
            'telegram',
            'wechat',
            'other_social_account'
        ]
        

class ContributeForm(ModelForm):
    """how to contribut for newton form"""
    def __init__(self, *args, **kw):
        super(ContributeForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'your_node_name',
            'your_node_organizer',
            'your_node_organizer_contact',
            'done_for_newton',
            'done_for_newton_attachment',
            'do_for_newton',
            'what_is_newton'
        ]
        
    class Meta:
        model = tokenexchange_models.KYCInfo
        fields = [
            'your_node_name',
            'your_node_organizer',
            'your_node_organizer_contact',
            'done_for_newton',
            'done_for_newton_attachment',
            'do_for_newton',
            'what_is_newton'
        ]
        

class EmergencyForm(ModelForm):
    """docstring for EmergencyForm"""
    cellphone_of_emergency_contact = user_forms.CellphoneGroupField(required=True, widget=user_forms.CellphoneGroupWidget, label='Emergency Cellphone')
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
