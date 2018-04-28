"""Service layer implementation for KYC administrator

"""
import logging

from django.conf import settings

from kyc import models as kyc_models

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
        allocated_address = kyc_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE).values_list('receive_btc_address', flat=True)
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
        allocated_address = kyc_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE).values_list('receive_ela_address', flat=True)
        avaiable_address = list(set(all_address).difference(set(allocated_address)))
        if not avaiable_address:
            logger.error("not available ELA address")
            return None
        return avaiable_address[0]
    except Exception, inst:
        logger.exception("fail to allocate ELA address:%s" % str(inst))
        return None

def send_distribution_letter(user):
    try:
        
        return True
    except Exception, inst:
        logger.exception("fail to send distribution letter:%s" % str(inst))
        return False
