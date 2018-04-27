# -*- coding: utf-8 -*-
import logging
from django.core.mail import EmailMessage
from celery import task
import time

logger = logging.getLogger(__name__)

@task()
def send_email(subject, content, from_email, to_emails, content_type='html'):
    try:
        msg = EmailMessage(subject, content, from_email, to_emails)
        msg.content_subtype = content_type
        msg.send()
    except Exception, inst:
        logger.error("fail to send email: %s" % str(inst))


