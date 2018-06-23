"""Service layer implementation for KYC administrator

"""
import logging
from hashlib import sha256

from django.conf import settings
from django.template import Template, Context, loader
from django.utils.translation import ugettext_lazy as _

from verification import services as verification_services
from tasks import task_email
from tokenexchange import models as tokenexchange_models
from config import codes
from utils import btc_validation

logger = logging.getLogger(__name__)

def __load_address_from_file(filename, coin):
    f = open(filename)
    all_address = []
    for line in f.readlines():
        line = line.strip()
        is_valid = False
        if coin == 'btc':
            if settings.USE_TESTNET:
                is_valid = btc_validation.validate(line, 0x6f)
            else:
                is_valid = btc_validation.validate(line)
        else:
            is_valid = btc_validation.validate(line, 0x21)
        if is_valid:
            all_address.append(line)
    return all_address

def allocate_btc_address():
    """Allocate the BTC address from address pool
    """
    try:
        all_address = __load_address_from_file(settings.BTC_WALLET_ADDRESS_FILE, "btc")
        allocated_address = tokenexchange_models.InvestInvite.objects.filter(phase_id=settings.CURRENT_FUND_PHASE).values_list('receive_btc_address', flat=True)
        avaiable_address = list(set(all_address).difference(set(allocated_address)))
        if not avaiable_address:
            logger.error("not available BTC address")
            return None
        return avaiable_address[0]
    except Exception, inst:
        logger.exception("fail to allocate BTC address:%s" % str(inst))
        return None

def allocate_ela_address():
    """Allocate the ela address from address pool
    """
    try:
        all_address = __load_address_from_file(settings.ELA_WALLET_ADDRESS_FILE, "ela")
        allocated_address = tokenexchange_models.InvestInvite.objects.filter(phase_id=settings.CURRENT_FUND_PHASE).values_list('receive_ela_address', flat=True)
        avaiable_address = list(set(all_address).difference(set(allocated_address)))
        if not avaiable_address:
            logger.error("not available ELA address")
            return None
        return avaiable_address[0]
    except Exception, inst:
        logger.exception("fail to allocate ELA address:%s" % str(inst))
        return None

def send_distribution_letter(user, request):
    """ Send distribution Letter to investor.
    """
    try:
        # build the email body
        email = user.email
        email_type = codes.EmailType.TEXCHANGE_DISTRIBUTE_AMOUNT_NOTIFY.value
        verification = verification_services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        target_url = "%s/tokenexchange/%s/" % (settings.NEWTON_HOME_URL, str(user.username))
        security_url = "%s/help/security/" % (settings.NEWTON_HOME_URL)
        subject = "NewtonProject Notification: KYC information is confirmed"
        template = loader.get_template("newtonadmin/distribution-letter.html")
        context = Context({"targetUrl": target_url,"request": request, "security_url": security_url})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send distribution letter:%s" % str(inst))
        return False

def send_kycinfo_notify(kyc_info, request):
    """Send the email letter for kyc pass info
    """
    try:
        # build the email body
        email = kyc_info.user.email
        email_type = codes.EmailType.TEXCHANGE_CONFIRM_KYC.value
        verification = verification_services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        if kyc_info.kyc_audit.is_pass:
            subject = "Newton Notification: You have passed the Newton KYC"
        else:
            subject = "Newton Notification: You are not passed the Newton KYC"
        template = loader.get_template("newtonadmin/kycinfo-notify-letter.html")
        security_url = "%s/help/security/" % (settings.NEWTON_HOME_URL)
        context = Context({"request":request, "kyc_info": kyc_info, 'security_url': security_url})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the apply amout notify:%s" % str(inst))        
        return False

def send_apply_amount_notify(invite_info, request):
    """Send the email letter for apply amount
    """
    try:
        # build the email body
        email = invite_info.user.email
        email_type = codes.EmailType.TEXCHANGE_INVITE_NOTIFY.value
        verification = verification_services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        target_url = "%s/tokenexchange/invite/%s/post/" % (settings.NEWTON_HOME_URL, invite_info.id)
        security_url = "%s/help/security/" % (settings.NEWTON_HOME_URL)
        subject = "Newton Notification: Fillout your expect amount"
        template = loader.get_template("newtonadmin/apply-amount-notify-letter.html")
        context = Context({"target_url": target_url, "request": request, "invite_info": invite_info, "security_url": security_url})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the apply amout notify:%s" % str(inst))        
        return False

def send_receive_confirm_notify(request, receive_info):
    """Send the email letter for receive amount.
    """
    try:
        # build the email body
        email = receive_info.user.email
        email_type = codes.EmailType.TEXCHANGE_RECEIVE_NOTIFY.value
        verification = verification_services.generate_verification_uuid(email, email_type)
        if not verification:
            logger.error("fail to generate verification object.")
            return False
        subject = _("Newton Notification: Receive Transferring Notification")
        template = loader.get_template("newtonadmin/receive-amount-notify-letter.html")
        context = Context({"request": request, "receive_info": receive_info})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the receive amout notify:%s" % str(inst))
        return False
