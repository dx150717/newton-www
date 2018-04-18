# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """   """

import os
import sys
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from config import codes
from user import services as user_services

class Command(BaseCommand):
    args = ''
    help = 'create user manually'
    def handle(self, *args, **options):
        if len(sys.argv) == 4:
            cellphone = args[0]
            password = args[1]
            result = user_services.create_user_by_admin(cellphone, password, cellphone[-4:], diamonds=10000)
            print "result:", result
        else:
            print "usage: %s :cellphone :password" % (sys.argv[0])
    
    
