# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """   """

import logging
import hashlib
import os

logger = logging.getLogger(__name__)

def md5_for_file(file_obj):
    md5 = hashlib.md5()
    for data in file_obj.chunks():
        md5.update(data)
    file_obj.seek(0)
    return md5.hexdigest()

def get_hashfile_dir_by_md5sum(md5sum):
    return os.path.join(md5sum[0:1], md5sum[1:2], md5sum[2:3])

def hashfile_upload_to(field_name, path_prefix=''):
    def upload_to(instance, filename):
        md5sum = md5_for_file(getattr(instance, field_name))
        basename, ext = os.path.splitext(filename)
        if not ext:
            ext = '.jpg'
        return os.path.join(path_prefix, get_hashfile_dir_by_md5sum(md5sum), md5sum + ext.lower())
    return upload_to

def normal_upload_to(field_name, path_prefix=''):
    def upload_to(instance, filename):
        md5sum = md5_for_file(getattr(instance, field_name).chunks())
        basename, ext = os.path.splitext(filename)
        return os.path.join(path_prefix, md5sum + ext.lower())
    return upload_to
