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

class MinimumAndRatioNode(template.Node):
    def __init__(self, item):
        self.item = template.Variable(item)

    def render(self, context):
        try:
            # Get the minimun amount and ratio
            item = self.item.resolve(context)
            phase_id = settings.CURRENT_FUND_PHASE
            token_exchange_info = settings.FUND_CONFIG[phase_id]
            min_btc = token_exchange_info['min_btc']
            btc_ratio = token_exchange_info['btc_ratio']
            min_ela = token_exchange_info['min_ela']
            ela_ratio = token_exchange_info['ela_ratio']
            # render template
            request = context['request']
            template = loader.get_template('tokenexchange/include-token-exchange-info.html')
            context = RequestContext(request, locals())
            html = template.render(context)
            return html
        except Exception, inst:
            logger.exception("fail to show the amount summary:%s" % str(inst))
            return ""

@register.tag(name='show_minimum_and_ratio')
def show_minimum_and_ratio(parser, token):
    """Show the amount summary for current phase
    """
    return MinimumAndRatioNode(token.split_contents()[1])


def exchange_assign_amount_to_NEW(assign_btc, assign_ela):
    """calculate amount to NEW
    """
    # get btc ratio and ela ratio
    phase_id = settings.CURRENT_FUND_PHASE
    token_exchange_info = settings.FUND_CONFIG[phase_id]
    btc_ratio = token_exchange_info['btc_ratio']
    ela_ratio = token_exchange_info['ela_ratio']
    # calculate exchange NEW
    btc_exchange_NEW = assign_btc * btc_ratio if assign_btc else 0
    ela_exchange_NEW = assign_ela * ela_ratio if assign_ela else 0
    return btc_exchange_NEW + ela_exchange_NEW
register.simple_tag(exchange_assign_amount_to_NEW)