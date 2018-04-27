
from django.template import Template, Context, loader
from django.conf import settings
from . import task 

def do_send_mail(subject, to_email, target_url, html_template, request):
    subject = subject
    targetUrl = target_url
    try:
        template = loader.get_template(html_template)
        context = Context({"targetUrl":targetUrl,"request":request})
        html_content = template.render(context)
        to_email = to_email
        from_email = settings.FROM_EMAIL
        task.send_email.delay(subject, html_content, from_email, [to_email])
        return True
    except Exception,inst:
        logger.error("fail to send email: %s" % str(inst))
        return False
