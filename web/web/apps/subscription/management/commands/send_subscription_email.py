# -*- coding: utf-8 -*-
import time
from tasks import task_email

from django.core.management.base import BaseCommand
from django.template import Context, loader
from django.conf import settings

from zinnia.views.entries import EntryDetail
from subscription import models as subscription_models
from config import codes

BATCH_SIZE = 3


class Command(BaseCommand):
    """Send subscribe emails
    """
    args = ''
    help = 'send subscribe emails'

    def print_usage(self):
        print "python manage.py send_subscription_email [article id] [email address|list] [[start index] [end index]]"

    def handle(self, *args, **options):
        try:
            # defined variable
            article_id = None
            email_list = []
            start_index = None
            end_index = None
            # handle params
            if len(args) < 2:
                self.print_usage()
                return
            if len(args) >= 2:
                article_id = int(args[0])
                email_list = args[1]
            if len(args) >= 3:
                start_index = int(args[2])
            if len(args) == 4:
                end_index = int(args[3])
                if start_index > end_index:
                    print 'start index bigger than end index'
                    return
            # get subscribe emails
            subscribe_emails = []
            if email_list != 'all':
                subscribe_emails = [item.strip() for item in email_list.split(',')]
            else:
                subscribe_emails = [item.email_address for item in subscription_models.SubscribedEmail.objects.filter(
                    status=codes.StatusCode.RELEASE.value,
                    is_spam=codes.SubscriptionEmailType.AVAILABLE.value).order_by('id')]
                if start_index is None and end_index is None:
                    pass
                elif start_index >= 0 and end_index is None:
                    subscribe_emails = subscribe_emails[start_index:]
                elif start_index >= 0 and end_index >= 0:
                    subscribe_emails = subscribe_emails[start_index:end_index]
            # get entry
            entry = EntryDetail().get_queryset().filter(id=article_id).first()
            if not entry:
                print "fail to search entry with entry id: %s" % article_id
                return None
            target_url = settings.BASE_URL + entry.get_absolute_url()
            base_url = settings.BASE_URL
            title = entry.title
            content = entry.content
            # render template
            template = loader.get_template("subscription/subscription-letter.html")
            context = Context({
                "target_url": target_url,
                "title": title,
                "content": content,
                "base_url": base_url,
            })
            html_content = template.render(context)
            # send email
            from_email = settings.FROM_EMAIL
            start_time = None
            for to_email in subscribe_emails:
                now_time = time.time()
                if start_time and now_time - start_time > 0.1:
                    task_email.send_email.delay(title, html_content, from_email, [to_email])
                    print "send success to email %s" % to_email
                else:
                    if start_time:
                        while now_time - start_time <= 0.1:
                            time.sleep(0.005)
                            now_time = time.time()
                    task_email.send_email.delay(title, html_content, from_email, [to_email])
                    print "send success to email %s" % to_email
                start_time = now_time
            print "send email successfully"
        except Exception, inst:
            print "fail to send email: %s" % str(inst)
