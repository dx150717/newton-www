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
    print "show amount summary is working"
    return AmountSummaryNode()

def level_choices():
    """return level choices list
    """
    try:
        return [i+1 for i in range(10)]
    except Exception, inst:
        logger.exception(str(inst))
        return ""

register.simple_tag(level_choices)