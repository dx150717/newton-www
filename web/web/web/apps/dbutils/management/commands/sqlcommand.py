import os
import sys
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection

class Command(BaseCommand):
    """Command for sql execute.
    """
    args = ''
    help = "Execute sql command."

    def print_usage(self):
        print "python manage.py sqlcommand <sql statement>"
        
    def handle(self, *args, **options):
        if len(args) != 1:
            self.print_usage()
            return
        sql = args[0]
        cursor = connection.cursor()
        cursor.execute(sql)

        
