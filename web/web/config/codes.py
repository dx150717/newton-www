# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """  """

from enum import Enum


class ErrorCode(Enum):
    FAIL = 0
    SUCCESS = 1
    UNAUTH = 2
    SIGN_ERROR = 3
    INVALID_PARAMS = 4
    MAINTAIN = 5
    UPGRADE = 6
    # common
    INVALID_AUTH = 100
    WRONG_PASSWORD = 101
    WRONG_CELLPHONE = 102
    INFORMAT_PASSWORD_CELLPHONE = 103
    BLOCK_USER = 104
    UNIT_USER_NOT_EXIST = 105
    WRONG_EMAIL = 106

class Language(Enum):
    CHINESE = 1
    ENGLISH = 2

class StatusCode(Enum):
    USER_DELETE = 0
    AVAILABLE = 1
    CANDIDATE = 2
    RELEASE = 3
    INTERVIEW = 4
    OFFER = 5
    CONTRACT = 6
    FIRE = 7
    CANCEL = 8
    CLOSE = 9
    REJECT = 10
    READ = 11
    INVALID = 12
    BLOCK = 13
    AUTO_CANCEL = 14

class UserFrom(Enum):
    DIRECT_REGISTER = 1
    QQ = 2
    WEIBO = 3
    WEIXIN = 4

class UserType(Enum):
    NORMAL = 1

class Gender(Enum):
    MALE = 1
    FEMALE = 2
    UNKNOWN = 3

class MembershipType(Enum):
    NORMAL = 1
    GOLD = 2
    PT = 3

class JobType(Enum):
    UNKNOWN = 1
    WORKING = 2
    NOWORK = 3

class EmailType(Enum):
    REGISTER = 1
    RESET = 2

class ConstructionType(Enum):
    UNKNOWN = 1
    UI = 2
    PROGRAM = 3

class KYCStatus(Enum):
    CANDIDATE = 1
    CONFIRM = 2
    CANCEL = 3
    DISTRIBUTE = 4
    SEND = 5

class FundPhase(Enum):
    PRIVATE = 1
    PUBLIC = 2
