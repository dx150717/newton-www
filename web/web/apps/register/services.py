"""Service Implementation of register module
"""
import logging

from tasks import task_email
from django.conf import settings
from django.template import Template, Context, loader

from verification import services

from config import codes
logger = logging.getLogger(__name__)


def send_register_validate_email(email, request):
    try:
        # build the email body
        email_type = codes.EmailType.REGISTER.value
        verification = services.generate_verification_uuid(email, email_type)
        target_url = settings.BASE_URL + "/register/verify/?uuid=" + str(verification.uuid)
        subject = "NewtonProject Notifications: Please Register Newton:"
        template = loader.get_template("register/register-letter.html")
        context = Context({"targetUrl":target_url,"request":request})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the register validate email:%s" % str(inst))
        return False
        
def get_register_verification_by_uuid(uuid):
    return services.generate_verification_uuid(uuid)
    
    
