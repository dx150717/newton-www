# -*- coding: utf-8 -*-
import logging
import datetime
from celery import task
import requests
import json
import decimal

from django.conf import settings

from config import codes
from tokenexchange import models as tokenexchange_models
from tracker import models as tracker_models

logger = logging.getLogger(__name__)

DECIMAL_SATOSHI = decimal.Decimal("100000000")

@task()
def sync_blockchain_data():
    """Sync the blockchain data
    """
    logger.debug("sync_blockchain_data:")
    try:
        for item in tokenexchange_models.InvestInvite.objects.filter(phase_id=settings.CURRENT_FUND_PHASE):
            # btc
            if item.receive_btc_address:
                txs = __get_btc_transactions(item.receive_btc_address)
                logger.debug(txs)
                for txid, value in txs:
                    if not tracker_models.AddressTransaction.objects.filter(txid=txid).first():
                        instance = tracker_models.AddressTransaction()
                        instance.user_id = item.user_id
                        instance.phase_id = item.phase_id
                        instance.address = item.receive_btc_address
                        instance.address_type = codes.CurrencyType.BTC.value
                        instance.txid = txid
                        instance.value = float(decimal.Decimal(str(value)) / DECIMAL_SATOSHI)
                        instance.save()
            # ela
            if item.receive_ela_address:
                txs = __get_ela_transactions(item.receive_ela_address)
                for txid, value in txs:
                    if not tracker_models.AddressTransaction.objects.filter(txid=txid).first():
                        instance = tracker_models.AddressTransaction()
                        instance.user_id = item.user_id
                        instance.phase_id = item.phase_id
                        instance.address = item.receive_ela_address
                        instance.address_type = codes.CurrencyType.ELA.value
                        instance.txid = txid
                        instance.value = float(decimal.Decimal(str(value)))
                        instance.save()
    except Exception, inst:
        logger.error("fail to sync blockchain data: %s" % str(inst))

def __get_btc_transactions(address):
    try:
        if not settings.USE_TESTNET:
            btc_url = settings.BTC_MAINNET_EXPLORER + '/rawaddr/%s'
        else:
            btc_url = settings.BTC_TESTNET_EXPLORER + '/rawaddr/%s'
        response = requests.get(btc_url % address)
        data = json.loads(response.text)
        if data['total_received'] <= 0:
            return []
        txs = data['txs']
        result = []
        now = datetime.datetime.now()
        for item in txs:
            out = item['out']
            txid = item['hash']
            dt = datetime.datetime.fromtimestamp(item['time'])
            # Ensure more than 6 confirmations
            if not settings.USE_TESTNET and now < (dt + datetime.timedelta(hours=1)):
                logger.info("pending transaction:%s" % txid)
                continue
            value = 0
            for tmp_item in out:
                if tmp_item.get('addr') == address: # found it
                    value += tmp_item['value']
            if value > 0:
                result.append([txid, value])
        return result
    except Exception, inst:
        logger.exception("fail to get btc transactions:%s" % str(inst))
        return None

def __get_ela_transactions(address):
    try:
        if not settings.USE_TESTNET:
            ela_url = settings.ELA_MAINNET_EXPLORER + '/api/v1/txs/?address=%s&pageNum=0'
        else:
            ela_url = settings.ELA_TESTNET_EXPLORER + '/api/v1/txs/?address=%s&pageNum=0'
        response = requests.get(ela_url % address)
        data = json.loads(response.text)
        txs = data['txs']
        result = []
        now = datetime.datetime.now()
        for item in txs:
            out = item['vout']
            txid = item['txid']
            dt = datetime.datetime.fromtimestamp(item['time'])
            # Ensure more than 6 confirmations
            if not settings.USE_TESTNET and now < (dt + datetime.timedelta(minutes=12)):
                logger.info("pending transaction:%s" % txid)
                continue
            value = 0
            for tmp_item in out:
                addresses = tmp_item['scriptPubKey']['addresses']
                if address in addresses: # found it
                    value += tmp_item['value']
            if value > 0:
                result.append([txid, value])
        return result
    except Exception, inst:
        logger.exception("fail to get ela transactions:%s" % str(inst))
        return None
