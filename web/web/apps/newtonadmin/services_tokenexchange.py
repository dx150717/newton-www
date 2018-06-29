"""Service layer implementation for KYC administrator

"""
import logging
from hashlib import sha256

from django.conf import settings
from django.utils import translation
from django.template import Template, Context, loader
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from verification import services as verification_services
from tasks import task_email
from tokenexchange import models as tokenexchange_models
from config import codes
from utils import btc_validation

logger = logging.getLogger(__name__)

def __load_address_from_file(filename, coin):
    f = open(filename)
    all_address = []
    btc_mainnet_prefix = [0x0, 0x5]
    btc_testnet_prefix = [0x6f, 0xc4]
    ela_mainnet_prefix = [0x21, 0x12]
    for line in f.readlines():
        line = line.strip()
        is_valid = False
        if coin == 'btc':
            if settings.USE_TESTNET:
                for prefix in btc_testnet_prefix:
                    is_valid = btc_validation.validate(line, prefix)
                    if is_valid:
                        break
            else:
                for prefix in btc_mainnet_prefix:
                    is_valid = btc_validation.validate(line, prefix)
                    if is_valid:
                        break
        else:
            for prefix in ela_mainnet_prefix:
                is_valid = btc_validation.validate(line, prefix)
                if is_valid:
                    break
        if is_valid:
            all_address.append(line)
    return all_address

def __select_language(user):
    if hasattr(user, 'userprofile'):
        translation.activate(user.userprofile.language_code)

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

def send_assign_letter(user, request):
    """ Send assign Letter to investor.
    """
    try:
        # build the email body
        email = user.email
        # check user's kyc_info
        kyc_info = tokenexchange_models.KYCInfo.objects.filter(user_id=user.id).first()
        print "kyc_info.first_name is %s" % kyc_info.first_name
        # select language by user's prefer language
        __select_language(user)
        target_url = "%s/user/" % (settings.NEWTON_HOME_URL)
        security_url = "%s/help/security/" % (settings.NEWTON_WEB_URL)
        subject = _("Please check the allocation of Newton token exchange")
        template = loader.get_template("newtonadmin/assign-letter.html")
        context = Context({"target_url": target_url,"request": request, "security_url": security_url, "kyc_info":kyc_info})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send assign letter:%s" % str(inst))
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
        # select language by user's prefer language
        user = kyc_info.user
        __select_language(user)
        # build email
        if kyc_info.kyc_audit.is_pass:
            subject = _("You have passed the Newton KYC")
        else:
            subject = _("You are not passed the Newton KYC")
        template = loader.get_template("newtonadmin/kycinfo-notify-letter.html")
        target_url = "%s/user/" % (settings.NEWTON_HOME_URL)
        security_url = "%s/help/security/" % (settings.NEWTON_WEB_URL)
        is_show_comment = False
        if kyc_info.kyc_audit.comment.strip():
            is_show_comment = True
        context = Context({"request":request, "kyc_info": kyc_info, 'security_url': security_url, "target_url": target_url, "codes": codes, "is_show_comment":is_show_comment})
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
        # select language by user's prefer language
        user = invite_info.user
        __select_language(user)
        # build email
        # target_url = "%s/tokenexchange/invite/%s/post/" % (settings.NEWTON_HOME_URL, invite_info.id)
        target_url = "%s/user/" % (settings.NEWTON_HOME_URL)
        security_url = "%s/help/security/" % (settings.NEWTON_WEB_URL)
        subject = _("Fillout your expect amount")
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
        # select language by user's prefer language
        user = receive_info.user
        __select_language(user)
        subject = _("Receive Transferring Notification")
        template = loader.get_template("newtonadmin/receive-amount-notify-letter.html")
        security_url = "%s/help/security/" % (settings.NEWTON_WEB_URL)
        context = Context({"request": request, "receive_info": receive_info, "security_url": security_url})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the receive amout notify:%s" % str(inst))
        return False
