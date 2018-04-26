# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class KYCInfo(models.Model):
    user = models.OneToOneField(User)
    
