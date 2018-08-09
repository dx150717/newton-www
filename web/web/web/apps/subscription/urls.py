from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', 'subscription.views.subscribe'),
                    url(r'confirmed/', 'subscription.views.subscribed_confirm')
                    
)