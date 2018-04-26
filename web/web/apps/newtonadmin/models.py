from django.db import models
from config import codes
from django.conf import settings
# Create your modelss here.

class KycModel(models.Model):
    first_name = models.CharField(default='', max_length=100)
    last_name = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=100, default='')
    country_code = models.CharField(max_length=100, default='')
    cellphone = models.CharField(max_length=100, default='')
    email = models.EmailField()
    id_card = models.ImageField(upload_to='avatar/%Y/%m/%d/')
    investment_btc = models.IntegerField()
    investment_ela = models.IntegerField()
    how_to_contribute = models.TextField()
    what_is_newton = models.TextField()
    btc_address = models.CharField(max_length=200, default='')
    ela_address = models.CharField(max_length=200, default='')
    btc_amount = models.FloatField()
    ela_amount = models.FloatField()
    pass_kyc = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
    uuid = models.CharField(default='1',db_index=True, max_length="200")
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name
    
    
    
