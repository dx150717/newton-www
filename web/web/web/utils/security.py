# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """


import uuid
import hashlib
import urllib
import collections

import cgi, base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

from django.conf import settings
from django.utils.http import urlquote
import random
import coder

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def generate_uuid():
    return str(uuid.uuid4().hex)


def generate_digest(data):
    return hashlib.md5(data).hexdigest()


def generate_digest_for_file(filename, block_size=2**20):
    md5 = hashlib.md5()
    f = open(filename)
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()

def sign_hmac(data, secret, prefix='', use_urlencode=False, joint='&'):
    data = collections.OrderedDict(sorted(data.items()))
    sign_string = prefix
    n = 0
    for k, v in data.items():
        if n != 0 and k != 'sign':
            sign_string += joint
        n += 1
        if k != 'sign':
            sign_string += u'%s=%s' % (k, v)
    sign_string += secret
    if use_urlencode:
        sign_string = urllib.quote_plus(sign_string)
    signed_string = generate_digest(sign_string)
    return signed_string

def generate_verify_code():
    """ Generate the 6-number verify code 
    """
    code = random.randint(100000, 999999)
    return code

def rsa_verify(data, pub_key, sign):
    key = RSA.importKey(pub_key)
    h = SHA.new(data)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, base64.b64decode(sign)):
        return True
    return False
