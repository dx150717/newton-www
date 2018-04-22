# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

from django import forms
from django.forms import ModelForm
from user.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
    
class UserProfileForm(ModelForm):
    first_name = forms.CharField(label="first_name", max_length=30, required=True)
    
    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        if hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
        self.fields.keyOrder = ['first_name', 'self_introduction', 'homepage', 'weibo', 'weixin', 'qq']
        
    class Meta:
        model = UserProfile
        fields = ['self_introduction', 'homepage', 'weibo', 'weixin', 'qq']
        
