# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

from django import forms
from django.forms import ModelForm
from user.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
    
class UserProfileForm(ModelForm):

        
    class Meta:
        model = UserProfile
        fields = ['gender', 'homepage', 'location', 'country_code', 'cellphone', 'job_status', 'construction_mode', 'self_introduction', 'channel', 'birth_date']
