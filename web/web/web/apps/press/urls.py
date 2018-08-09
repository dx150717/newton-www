from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.PressView.as_view(), name='press'),
)