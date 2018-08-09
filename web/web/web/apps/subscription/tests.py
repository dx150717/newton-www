from django.test import TestCase

from . import models as sub_models

def create_data():
    sub_models.SubscribedEmail.objects.create(email_address="1111111111@163.com", uuid="111111", status=3)
    sub_models.SubscribedEmail.objects.create(email_address="2222222222@163.com", uuid="222222", status=3)
    sub_models.SubscribedEmail.objects.create(email_address="3333333333@163.com", uuid="333333", status=3)
    sub_models.SubscribedEmail.objects.create(email_address="4444444444@163.com", uuid="444444", status=3)
    sub_models.SubscribedEmail.objects.create(email_address="5555555555@163.com", uuid="555555", status=3)
    sub_models.SubscribedEmail.objects.create(email_address="6666666666@163.com", uuid="666666", status=3)
    sub_models.SubscribedEmail.objects.create(email_address="7777777777@163.com", uuid="777777", status=3)
    sub_models.SubscribedEmail.objects.create(email_address="8888888888@163.com", uuid="888888", status=3)
    sub_models.SubscribedEmail.objects.create(email_address="9999999999@163.com", uuid="999999", status=3)
