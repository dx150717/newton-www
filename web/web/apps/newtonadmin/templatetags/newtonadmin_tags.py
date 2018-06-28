# -*- coding: utf-8 -*-
import logging
import re
import datetime

from django import template
from django.conf import settings
from django.utils import translation
from django.utils.translation import ungettext as _
from django.utils.safestring import mark_safe
from django.utils.timezone import utc
from django.template import Context
from django.template import loader
from django.template import RequestContext
from django.db.models import Sum
from django.contrib.auth.models import User

from config import codes
from tracker import models as tracker_models
from tokenexchange import models as tokenexchange_models

logger = logging.getLogger(__name__)
register = template.Library()

class AmountSummaryNode(template.Node):
    def __init__(self):
        pass
    
    def render(self, context):
        try:
            # Get the total amount
            phase_id = settings.CURRENT_FUND_PHASE
            token_exchange_info = settings.FUND_CONFIG[phase_id]
            total_btc_amount = token_exchange_info['total_amount_btc']
            total_ela_amount = token_exchange_info['total_amount_ela']
            # caculate btc current allocated amount
            total_assign_btc = tokenexchange_models.InvestInvite.objects.all().aggregate(Sum('assign_btc'))
            total_assign_btc = total_assign_btc.get("assign_btc__sum", 0)
            if not total_assign_btc:
                total_assign_btc = 0
            btc_remain_amount = total_btc_amount - total_assign_btc
            # caculate ela current allocated amount
            total_assign_ela = tokenexchange_models.InvestInvite.objects.all().aggregate(Sum('assign_ela'))
            total_assign_ela = total_assign_ela.get("assign_ela__sum", 0)
            if not total_assign_ela:
                total_assign_ela = 0
            ela_remain_amount = total_ela_amount - total_assign_ela
            # render template
            request = context['request']
            template = loader.get_template('newtonadmin/include-amount-summary.html')
            context = RequestContext(request, locals())
            html = template.render(context)
            return html
        except Exception, inst:
            logger.exception("fail to show the amount summary:%s" % str(inst))
            return ""

@register.tag(name='show_amount_summary')
def show_amount_summary(parser, token):
    """Show the amount summary for current phase
    """
    return AmountSummaryNode()

AUDIT_CODES_AND_OPERATION = {
    codes.AdminActionType.PASS_KYC.value : u'通过',
    codes.AdminActionType.REJECT_KYC.value : u'驳回',
    codes.AdminActionType.DENY_KYC.value : u'拒绝',
    codes.AdminActionType.INVITE.value : u'邀请填写申请数量',
    codes.AdminActionType.SEND_INVITE.value : u'发送邀请邮件',
    codes.AdminActionType.ASSIGN_AMOUNT.value : u'填写分配数量',
    codes.AdminActionType.CONFIRM_AMOUNT.value : u'确认分配数量',
    codes.AdminActionType.SEND_CONFIRM_EMAIL.value : u'发送收币确认邮件',
}

def show_audit_operation(audit_code):
    """Show the audit operation
    """
    try:
        for k, v in AUDIT_CODES_AND_OPERATION.items():
            if audit_code == k:
                return v
    except Exception, inst:
        logger.exception("fail to show the audit operation:%s" % str(inst))
        return ""
register.simple_tag(show_audit_operation)

def show_audit_email(audit_id):
    """Show the audit email address
    """
    try:
        admin_user_info = User.objects.filter(id=audit_id).first()
        return admin_user_info.email
    except Exception, inst:
        logger.exception("fail to show the audit email address:%s" % str(inst))
        return ""
register.simple_tag(show_audit_email)