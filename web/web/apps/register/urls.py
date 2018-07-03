from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.submit_email, name="submit_email"),
                       #url(r'^email/post/$', views.submit_email, name="submit_email"),
                       url(r'^email/success/$', views.show_post_email_success_view, name="show_post_email_success_view"),
                       url(r'^email/fail/$', views.show_post_email_fail_view, name="show_post_email_fail_view"),
                       url(r'^email/verify/$', views.verify_email_link, name="verify_email_link"),
                       url(r'^invalid-link/', views.show_invalid_link_view, name="show_invalid_link_view"),
                       url(r'^password/$', views.show_password_view, name="show_password_view"),
                       url(r'^password/post/$', views.submit_password, name="submit_password"),
                       url(r'^success/$', views.show_register_success_view),
)
