from django.shortcuts import render

import json
import re
import logging
from django.http import HttpResponse
from django.template import Template,Context,loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from ratelimit.decorators import ratelimit
from subscription import models as subscription_model
from config import codes
from utils import http,security
from django.conf import settings
import task as subscription_task

logger = logging.getLogger(__name__)

#@ratelimit(key='ip', rate='1/m', method=['GET','POST'])
def subscribe(request):
    """
    Add email address to email list database.
    User can add email once per minute.
    """
    try:
        was_limited = getattr(request, 'limited', False)
        if not was_limited:
            email_address = request.POST['email_address']
            validate_email(email_address)
            subscribed_email = subscription_model.SubscribedEmail.objects.filter(email_address = email_address).first()
            if subscribed_email:
                if subscribed_email.status == codes.StatusCode.RELEASE.value:
                    result = http.JsonErrorResponse(error_message = _('Email Has Exist!'))
                else:
                    send_flag = do_send_mail(subscribed_email,request)
                    if send_flag:
                        result = http.JsonSuccessResponse(data = {"msg": _("we've sent you a confirming e-mail,please check your email box.")})
                    else:
                        result = http.JsonErrorResponse(error_message = _("Subscribe Failed!"))
            else:
                subscribed_email = subscription_model.SubscribedEmail(email_address = email_address)
                subscribed_email.uuid = security.generate_uuid()
                subscribed_email.save()
                send_flag = do_send_mail(subscribed_email,request)
                if send_flag:
                    result = http.JsonSuccessResponse(data = {"msg": _("we've sent you a confirming e-mail,please check your email box.")})
                else:
                    result = http.JsonErrorResponse(error_message = _("Subscribe Failed!"))
        else:
            result = http.JsonErrorResponse(error_message = _("You can only subscribe once per minute."))
        return result
    except ValidationError:
        return http.JsonErrorResponse(error_message = _("Invalid Email Address!"))
    except Exception, inst:
        logger.exception('error unknown : %s' % str(inst))
        return http.JsonErrorResponse()


def subscribed_confirm(request):
    try:
        email_address = request.GET['u']
        subscribed_email = subscription_model.SubscribedEmail.objects.filter(uuid = email_address).first()
        if subscribed_email:
            code = subscribed_email.status
            if code == codes.StatusCode.AVAILABLE.value:
                subscribed_email.status = codes.StatusCode.RELEASE.value
                subscribed_email.save()
            return render(request, 'subscription/confirm.html')
        else:
            logger.error("fail to find email by uuid: %s" % str(inst))
            return http.JsonErrorResponse()
    except Exception, inst:
        logger.error("fail to confirm email: %s" % str(inst))
        return http.JsonErrorResponse()

def do_send_mail(subscribed_email,request):
    subject = _("NewtonProject Notifications: Please Confirm Subscription")
    targetUrl = settings.BASE_URL + "/subscribe/confirmed/?u=" + str(subscribed_email.uuid)
    try:
        template = loader.get_template("subscription/subscription-letter.html")
        context = Context({"targetUrl":targetUrl,"request":request})
        html_content = template.render(context)
        to_email = subscribed_email.email_address
        from_email = settings.FROM_EMAIL
        subscription_task.send_email.delay(subject,html_content,from_email,[to_email])
        return True
    except Exception,inst:
        logger.error("fail to send email: %s" % str(inst))
        return False
