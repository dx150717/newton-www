# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

import re
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation.trans_real import get_supported_language_variant
from django.utils.translation import ugettext_lazy as _

GLOBAL_PHONE_PATTERN = re.compile(r'^\d{6,15}$')

PHONE_PATTERN = re.compile(r'^(1)(3\d{2}|4[579]\d|5[0-35-9]\d|7[0135678]\d|8\d{2})(\d{3})(\d{4})$')


def is_valid_cellphone(cellphone, country_code=None):
    cellphone = str(cellphone)
    if settings.CELLPHONE_WILDCARD_PREFIX and len(cellphone) == 11 and cellphone.startswith(settings.CELLPHONE_WILDCARD_PREFIX):
        return True
    if country_code and country_code != settings.CHINA_COUNTRY_CALLING_CODE:
        return GLOBAL_PHONE_PATTERN.match(country_code+cellphone)
    else:
        return PHONE_PATTERN.match(cellphone)


def get_character_length(value):
    cur_len = 0
    for i in range(len(value)):
        if ord(value[i]) < 128:
            cur_len += 1
        else:
            cur_len += 2
    return cur_len


def is_valid_language_code(lc):
    try:
        get_supported_language_variant(lc)
    except LookupError:
        return False
    return True

def validate_file_extension_of_id_photo(value):
    """
    Validate file's type by value which input is file's name.
    """
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_(u'Unsupported file extension.'))

def validate_file_size_of_id_photo(value):
    """
    Validate file's size by value which input is file's size.
    """
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_(u'File too large,Size should not exceed 5M'))

def valid_password(value):
    """Validate whether password contains upercase, lowercase and number 
    """
    if not re.search('[A-Z]', value) or not re.search('[a-z]', value) or not re.search('[0-9]', value):
        raise ValidationError(_(u'Please input 6～16 characters，must contain upper-case, lower-case letters and numbers.'))