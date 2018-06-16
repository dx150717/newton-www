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
from django.template import Context, loader

from config import codes

logger = logging.getLogger(__name__)
register = template.Library()

class AmountSummaryNode(template.Node):
    def __init__(self):
        pass
    
    def render(self, context):
        try:
            phase_id = settings.phase_id
            # Get the total amount
            # caculate the current allocated amount
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
    return AmountSummaryNode(token.split_contents()[1])
