# -*- coding: utf-8 -*-
import time
from tasks import task_email

from django.utils.translation import ugettext as _
from django.core.management.base import BaseCommand
from django.template import Context, loader
from django.conf import settings

from zinnia.views.entries import EntryDetail
from subscription import models as subscription_models
from zinnia.managers import CHINESE, ENGLISH

class Command(BaseCommand):
    """Send subscribe emails
    """
    args = ''
    help = 'send subscribe emails'

    def print_usage(self):
        print "python manage.py weekly_report [article id] [email address|list]"

    def handle(self, *args, **options):
        try:
            if len(args) != 2:
                self.print_usage()
                return
            article_id = int(args[0])
            email_list = args[1]
            subscribe_emails = []
            if email_list != 'all':
                subscribe_emails = [item.strip() for item in email_list.split(',')]
            else:
                subscribe_emails = subscription_models.SubscribedEmail.objects.values_list('email_address', flat=True)
            entry = EntryDetail().get_queryset().filter(id=article_id).first()
            if not entry:
                print "fail to search entry with entry id: %s" % article_id
                return None
            target_url = settings.BASE_URL + entry.get_absolute_url()
            base_url = settings.BASE_URL
            title = entry.title
            content = entry.content
            template = loader.get_template("newtonadmin/subscription-letter.html")
            context = Context({
                "target_url": target_url,
                "title": title,
                "content": content,
                "base_url": base_url,
            })
            html_content = template.render(context)
            for to_email in subscribe_emails:
                from_email = settings.FROM_EMAIL
                task_email.send_email.delay(title, html_content, from_email, [to_email])
                print "send email to %s successfully" % to_email
        except Exception, inst:
            print "fail to send email: %s" % str(inst)