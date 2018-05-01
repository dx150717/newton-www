"""Service layer implementation for KYC administrator

"""
import logging

from django.conf import settings
from django.template import Template, Context, loader

from verification import services
from tasks import task_email
from tokenexchange import models as tokenexchange_models
from config import codes

logger = logging.getLogger(__name__)

def __load_address_from_file(filename):
    f = open(filename)
    all_address = []
    for line in f.readlines():
        line = line.strip()
        if len(line) == 34:
            all_address.append(line)
    return all_address

def allocate_btc_address():
    """Allocate the BTC address from address pool
    """
    try:
        all_address = __load_address_from_file(settings.BTC_WALLET_ADDRESS_FILE)
        allocated_address = tokenexchange_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE).values_list('receive_btc_address', flat=True)
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
        all_address = __load_address_from_file(settings.ELA_WALLET_ADDRESS_FILE)
        allocated_address = tokenexchange_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE).values_list('receive_ela_address', flat=True)
        avaiable_address = list(set(all_address).difference(set(allocated_address)))
        if not avaiable_address:
            logger.error("not available ELA address")
            return None
        return avaiable_address[0]
    except Exception, inst:
        logger.exception("fail to allocate ELA address:%s" % str(inst))
        return None

def send_distribution_letter(user, request):
    try:
        # build the email body
        email = user.email
        email_type = codes.EmailType.TEXCHANGE_DISTRIBUTE_AMOUNT_NOTIFY.value
        verification = services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        target_url = "%s/tokenexchange/%s/" % (settings.BASE_URL, str(user.username))
        subject = "NewtonProject Notifications: KYC information is confirmed:"
        template = loader.get_template("newtonadmin/distribution-letter.html")
        context = Context({"targetUrl":target_url,"request":request})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send distribution letter:%s" % str(inst))
        return False

def send_apply_amount_notify(user, request):
    """Send the email letter for apply amount
    """
    try:
        # build the email body
        email = user.email
        email_type = codes.EmailType.TEXCHANGE_APPLY_AMOUNT.value
        verification = services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        target_url = "%s/tokenexchange/apply/" % (settings.BASE_URL)
        subject = "NewtonProject Notifications: Apply the amount:"
        template = loader.get_template("newtonadmin/apply-amount-notify-letter.html")
        context = Context({"target_url":target_url,"request":request})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the apply amout notify:%s" % str(inst))        
        return False

def send_confirm_distribution_notify(item, request):
    """Send the email letter for confirm distribution
    """
    try:
        # build the email body
        email = item.user.email
        email_type = codes.EmailType.TEXCHANGE_DISTRIBUTE_AMOUNT_NOTIFY.value
        verification = services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        target_url = "%s/tokenexchange/confirm/" % (settings.BASE_URL)
        subject = "NewtonProject Notifications: Confirm the distribution:"
        template = loader.get_template("newtonadmin/confirm-distribution-notify-letter.html")
        context = Context({"target_url":target_url,"request":request, "item":item})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the confirm distribution notify:%s" % str(inst))        
        return False
