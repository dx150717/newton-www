# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """  """

from django.contrib.auth import get_user_model


class EmailAuthBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        if username is None:
            return None
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class PhoneAuthBackend(object):
    def authenticate(self, phone_no=None, password=None, **kwargs):
        UserModel = get_user_model()
        if phone_no is None:
            return None
        try:
            user = UserModel.objects.get(phone_no=phone_no)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
