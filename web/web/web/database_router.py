#-*- coding:utf-8 -*-
""" Database Router
"""

from django.conf import settings


class NewtonRouter(object):
    """
    NewtonRouter to control all database operations on models
    in the newton application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read tokenexchange models go to tokenexchange_db.
        """
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write tokenexchange models go to tokenexchange_db.
        """
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a models in the newton app is involved.
        """
        obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if obj1 and obj2:
            if obj1 == obj2:
                return True
            else:
                return False
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure that apps only appear in the related database.
        """
        if db in settings.DATABASE_APPS_MAPPING.values():
            return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label) == db
        elif model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return False
        return None
