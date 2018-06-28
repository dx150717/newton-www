"""Service Implementation of kyc module
"""
import time
import datetime
import logging

from django.conf import settings
from django.template import Template, Context, loader
from django.utils.translation import ugettext as _
from django.utils.timezone import utc

from verification import services
from tasks import task_email
from config import codes

logger = logging.getLogger(__name__)


def send_kyc_confirm_email(kyc_info, request):
    """Send the confirm email for user kyc
    """
    try:
        # build the email body
        email = kyc_info.user.email
        email_type = codes.EmailType.TEXCHANGE_CONFIRM_KYC.value
        verification = services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        subject = _("Received your KYC information")
        template = loader.get_template("tokenexchange/receive-kyc-notify-letter.html")
        context = Context({"request":request, 'kyc_info':kyc_info})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the kyc confirm email:%s" % str(inst))
        return False
        
def is_beyond_apply_deadline():
    """check whether it is beyond the deadline of applying amount
    """
    now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
    phase_id = settings.CURRENT_FUND_PHASE
    token_exchange_info = settings.FUND_CONFIG[phase_id]
    deadline = datetime.datetime.strptime(token_exchange_info["end_date"], "%Y-%m-%d %H:%M")
    dead_time = deadline.replace(tzinfo=utc)
    if now_time > dead_time:
        return True
    return False