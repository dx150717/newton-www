from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.show_reset_view),
                    url(r'^post_email/', views.post_email),
                    url(r'^reset_password/', views.show_reset_password_view),
                    url(r'^post_password/', views.post_password),
)