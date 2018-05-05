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
from django.contrib.auth.models import User

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
        return [None, None]

    def format_output(self, rendered_widgets):
        return ('''
        <div class="form-inline">
            <label>%s %s</label>
        </div>''') % tuple(rendered_widgets)
        


class CellphoneGroupField(forms.MultiValueField):
    widget = CellphoneGroupWidget

    def __init__(self, *args, **kwargs):
        fields = (forms.CharField(label=_("Country Code")), forms.CharField(label=_("Cellphone")))
        super(CellphoneGroupField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['email']