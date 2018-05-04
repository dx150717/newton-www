from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.show_register_view, name="index"),
                       url(r'^post-email/', views.submit_email, name="submit_email"),
                       url(r'^post-success/', views.show_post_email_success_view, name="show_post_email_success_view"),
                       url(r'^post-fail/', views.show_post_email_fail_view, name="show_post_email_fail_view"),
                       url(r'^verify/', views.verify_email_link, name="verify_email_link"),
                       url(r'^invalid-link/', views.show_invalid_link_view, name="show_invalid_link_view"),
                       url(r'^password/$', views.show_password_view, name="show_password_view"),
                       url(r'^password/submit/', views.submit_password, name="submit_password"),
                       url(r'^register-success/$', views.show_register_success_view),
)
