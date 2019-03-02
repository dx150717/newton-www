# -*- coding: utf-8 -*-

__author__ = 'chenpengtao@diynova.com'
__version__ = '$Rev$'
__doc__ = """   """

import logging

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from .internal_api import InternalAPIService
from .internal_api import ttypes

logger = logging.getLogger(__name__)


class InternalAPIClient(object):
    """
    Client for invoking internal thrift-style API
    """

    def __init__(self, host, port):
        # Make socket
        self.socket = TSocket.TSocket(host, port)
        # Buffering is critical. Raw sockets are very slow
        self.transport = TTransport.TFramedTransport(self.socket)
        # Wrap in a protocol
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        # Create a client to use the protocol encoder
        self.client = InternalAPIService.Client(self.protocol)

    def send_sms(self, country_code, cellphone, content, queue='default', priority=5):
        """ Send code message.

        :param string country_code: Mobile phone number national identification code
        :param string cellphone: Phone number
        :param string content: the content of sms
        :param string queue: The name of celery queue
        :param int priority: The priority of celery queue
        :return: The Code or False
        """
        self.transport.open()
        result = self.client.send_sms(country_code, cellphone, content, queue, priority)
        self.transport.close()
        return result

    def send_email(self, subject, content, from_email, to_emails, content_type='html', queue='default', priority=5):
        """ Send email.

        :param string subject: email's subject
        :param string content: email's content
        :param string from_email: The sender of email
        :param list or tuple to_emails: The recipient of email
        :param content_type: content's type
        :param string queue: The name of celery queue
        :param int priority: The priority of celery queue
        :return: True or False
        """
        self.transport.open()
        result = self.client.send_email(subject, content, from_email, to_emails, content_type, queue, priority)
        self.transport.close()
        return result

    def web_push(self, head, body, icon, url, group, ttl):
        """ web push.

        :param head: the head of web push
        :param body: the body of web push
        :param icon: the icon of web push
        :param url: the url of web push
        :param group: the group of web push
        :param int ttl: the ttl of web push
        :return: True or False.
        """
        self.transport.open()
        result = self.client.web_push(head, body, icon, url, group, ttl)
        self.transport.close()
        return result

    def web_push_v1(self, head, body, icon, url, group, ttl, queue='default', priority=5):
        """ web push.

        :param head: the head of web push
        :param body: the body of web push
        :param icon: the icon of web push
        :param url: the url of web push
        :param group: the group of web push
        :param int ttl: the ttl of web push
        :param string queue: The name of celery queue
        :param int priority: The priority of celery queue
        :return: True or False.
        """
        self.transport.open()
        result = self.client.web_push_v1(head, body, icon, url, group, ttl, queue, priority)
        self.transport.close()
        return result

    def create_app_push_information(self, address, active, push_service_type, wallet_type, registration_id,
                                    application_id, language):
        self.transport.open()
        result = self.client.create_app_push_information(address, active, push_service_type, wallet_type,
                                                         registration_id, application_id, language)
        self.transport.close()
        return result

    def update_app_push_information(self, address, push_service_type, application_id,
                                    old_registration_id, new_registration_id):
        self.transport.open()
        result = self.client.update_app_push_information(address, push_service_type, application_id,
                                                         old_registration_id, new_registration_id)
        self.transport.close()
        return result

    def delete_app_push_information(self, address, push_service_type, registration_id, application_id):
        self.transport.open()
        result = self.client.delete_app_push_information(address, push_service_type, registration_id, application_id)
        self.transport.close()
        return result

    def app_push(self, data, queue='default', priority=5):
        self.transport.open()
        result = self.client.app_push(data, queue, priority)
        self.transport.close()
        return result

    def add_upgrade_data(self, app_id, platform_type, version, version_code, is_force_upgrade,
                         is_show, message, download_url, language_code, status):
        """ Add NewPay upgrade information.

        :param app_id: Mobile application type
        :param platform_type: Mobile phone system type
        :param version: The version number
        :param version_code: The version number
        :param is_force_upgrade: Whether to force upgrade
        :param is_show: Whether to display upgrade information
        :param message: Upgrade information
        :param download_url: Application download link
        :param language_code: Language type
        :param status: Status
        :return: True or False
        """
        self.transport.open()
        result = self.client.add_upgrade_data(
            app_id, platform_type, version, version_code, is_force_upgrade,
            is_show, message, download_url, language_code, status)
        self.transport.close()
        return result

    def query_upgrade_data(self, platform_type, page_id):
        """ Query NewPay upgrade information.

        :param platform_type: Mobile system platform
        :param page_id: The page number you chose
        :return:
        """
        self.transport.open()
        result = self.client.query_upgrade_data(platform_type, page_id)
        self.transport.close()
        return result

    def del_upgrade_data(self, id_upgrade_data):
        """ Delete NewPay upgrade information.

        :param id_upgrade_data: The id of upgrade_data.
        :return:
        """
        self.transport.open()
        result = self.client.del_upgrade_data(id_upgrade_data)
        self.transport.close()
        return result
