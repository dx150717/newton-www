#-*- coding: utf-8 -*-
"""Service Implementation of register module
"""
import logging

from django.conf import settings
from django.template import Template, Context, loader
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from verification import services
from user import models as user_models
from tasks import task_email
from config import codes

logger = logging.getLogger(__name__)

def send_register_validate_email(email, request):
    """Send the validate email for user register
    """
    try:
        # build the email body
        email_type = codes.EmailType.REGISTER.value
        verification = services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        target_url = "%s/register/email/verify/?uuid=%s" % (settings.NEWTON_HOME_URL, str(verification.uuid))
        security_url = "%s/help/security/" % (settings.NEWTON_WEB_URL)
        subject = _("Newton Notification: Please complete the register process of Newton")
        template = loader.get_template("register/register-letter.html")
        context = Context({"target_url":target_url,"request":request, "security_url":security_url})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the register validate email:%s" % str(inst))
        return False
        
def get_register_verification_by_uuid(uuid):
    """Get the verification object of register by uuid
    """
    return services.get_verification_by_uuid(uuid)

def create_user(username, email, password, language_code, verification):
    """Create User
    """
    try:
        user = User.objects.create_user(username, email)
        user.set_password(password)
        user.save()
        user_profile = user_models.UserProfile.objects.create(user=user)
        user_profile.language_code = language_code
        user_profile.save()
        verification.status = codes.StatusCode.CLOSE.value
        verification.save()
        return True
    except Exception, inst:
        logger.exception("fail to create user:%s" % str(inst))
        return False
    
    
