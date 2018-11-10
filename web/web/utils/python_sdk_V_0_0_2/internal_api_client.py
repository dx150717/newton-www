# -*- coding: utf-8 -*-

__author__ = 'chenpengtao@diynova.com'
__version__ = '$Rev$'
__doc__ = """   """

import logging

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from .internal_api import InternalAPIService

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

    def send_email(self, subject, content, from_email, to_emails, content_type='html'):
        """  Send email.

        :param string subject: email's subject
        :param string content: email's content
        :param string from_email: The sender of email
        :param list or tuple to_emails: The recipient of email
        :param content_type: content's type
        :return: True or False
        """
        self.transport.open()
        result = self.client.send_email(subject, content, from_email, to_emails, content_type)
        self.transport.close()
        return result

    def send_code_message(self, country_code, cellphone):
        """ Send code message.

        :param string country_code: Mobile phone number national identification code
        :param string cellphone: Phone number
        :return: True or False
        """
        self.transport.open()
        result = self.client.send_code_message(country_code, cellphone)
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
        :return: The result for upgrade information.
        """
        self.transport.open()
        result = self.client.query_upgrade_data(platform_type, page_id)
        self.transport.close()
        return result

    def del_upgrade_data(self, id_upgrade_data):
        """ Delete NewPay upgrade information.
        :return: True or False.
        """
        self.transport.open()
        result = self.client.del_upgrade_data(id_upgrade_data)
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
