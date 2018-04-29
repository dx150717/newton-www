# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from user.models import UserProfile


    
class UserProfileForm(ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['gender', 'homepage', 'location', 'country_code', 'cellphone', 'job_status', 'major', 'self_introduction', 'channel', 'birth_date']
        widgets = {'birth_date': forms.TextInput(attrs={'type':'date'}),}