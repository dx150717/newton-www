# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

from django import forms
from django.forms import ModelForm
from django.forms import MultiWidget
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from user.models import UserProfile

class CellphoneGroupWidget(MultiWidget):
    
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs)
        ]
        super(CellphoneGroupWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.country_code, value.cellphone]
        return [settings.CHINA_COUNTRY_CALLING_CODE, None]

    def format_output(self, rendered_widgets):
        return ('''
        <div class="form-inline">
            <label>%s %s</label>
        </div>''') % tuple(rendered_widgets)
        


class CellphoneGroupField(forms.MultiValueField):
    widget = CellphoneGroupWidget

    def __init__(self, *args, **kwargs):
        fields = (forms.CharField(), forms.CharField())
        super(CellphoneGroupField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list


class UserProfileForm(ModelForm):
    cellphone_group = CellphoneGroupField(label=_('cellphone'),required=True, widget=CellphoneGroupWidget)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        country_code_widget = self.fields['cellphone_group'].widget.widgets[0]
        cellphone_widget = self.fields['cellphone_group'].widget.widgets[1]
        instance = kwargs['instance'] if kwargs.has_key('instance') else None
        if instance:
            country_code = instance.country_code
            cellphone = instance.cellphone
            self.fields['cellphone_group'].initial = [country_code, cellphone]
        
        
    class Meta:
        model = UserProfile
        fields = ['gender', 'homepage','location', 'cellphone_group', 'job_status', 'major', 'self_introduction', 'channel', 'birth_date']
        widgets = {'birth_date': forms.TextInput(attrs={'type':'date'})}