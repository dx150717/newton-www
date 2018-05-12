# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

import copy
import re

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
        pattern = re.compile('placeholder="*"', re.IGNORECASE)
        w1 = str(rendered_widgets[0])
        w1 = pattern.sub('placeholder="%s"' % unicode(_("Area Code")), w1)
        w2 = str(rendered_widgets[1])
        w2 = pattern.sub('placeholder="%s"' % unicode(_("Phone Number")), w2)
        new_widgets = [w1, w2]
        return ('''
        <div class="form-inline">
            <div>%s %s</div>
        </div>''') % tuple(new_widgets)


class CellphoneGroupField(forms.MultiValueField):
    widget = CellphoneGroupWidget

    def __init__(self, *args, **kwargs):
        fields = (forms.CharField(), forms.CharField())
        super(CellphoneGroupField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['email']
