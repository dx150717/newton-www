# -*- coding: utf-8 -*-
"""
Utility for create admin user

"""

__copyright__ = """ Copyright (c) 2016 Beijing ShenJiangHuDong Technology Co., Ltd. All rights reserved."""
__version__ = '1.0'
__author__ = 'xiawu@lubangame.com'

import logging
import os
import sys
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from config import codes
from user import services as user_services

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'create admin user manually'
    def handle(self, *args, **options):
        if len(sys.argv) == 4:
            email = args[0]
            password = args[1]
            result = user_services.create_admin_user(email, password)
            print "result:", result
        else:
            print "usage: %s :cellphone :password" % (sys.argv[0])
    
    
