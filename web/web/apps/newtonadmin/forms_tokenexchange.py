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

class PostInviteForm(forms.Form):
    user_id = forms.IntegerField(required=True)

class KYCQueryForm(forms.Form):
    KYC_TYPE_OPTIONS = (
        (codes.KYCType.INDIVIDUAL.value, u'个人'),
        (codes.KYCType.ORGANIZATION.value, u'机构'),
    )
    NODE_OPTIONS = (
        (1, u'是'),
        (0, u'否'),
    )
    EXCLUDE_COUNTRY = (
        ('', u'------'),
        ('CN', u'中国除外'),
        ('US', u'美国除外'),
        ('CN, US', u'中国和美国除外'),
    )
    kyc_type = forms.ChoiceField(widget=forms.Select, choices=KYC_TYPE_OPTIONS, label=u'主体类型')
    is_establish_node = forms.ChoiceField(widget=forms.Select, choices=NODE_OPTIONS, label=u'是否建立社群节点')
    country = CountryField().formfield(label=u'国家')
    exclude_country = forms.ChoiceField(widget=forms.Select, choices=EXCLUDE_COUNTRY, label=u'主体类型')