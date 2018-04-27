from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.show_reset_view),
                    url(r'^post-email/', views.post_email),
                    url(r'^post-success/', views.show_post_success_view),
                    url(r'^post-fail/', views.show_post_fail_view),
                    url(r'^verify/', views.verify_email_link),
                    url(r'^invalid-link/', views.show_invalid_link_view),
                    url(r'^reset-password/', views.show_reset_password_view),
                    url(r'^post-password/', views.post_password),
)