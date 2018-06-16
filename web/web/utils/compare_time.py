# -*- coding: utf-8 -*-
import time
import datetime

from django.utils.timezone import utc

from django.conf import settings


def compare_now_with_deadline():
    now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
    phase_id = settings.CURRENT_FUND_PHASE
    token_exchange_info = settings.FUND_CONFIG[phase_id]
    kyc_deadline = time.strptime(token_exchange_info["kyc_deadline"], "%Y-%m-%d")
    dead_time = datetime.datetime(*kyc_deadline[:6]).replace(tzinfo=utc)
    if now_time > dead_time:
        return True
    return False