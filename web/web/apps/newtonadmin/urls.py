from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.index, name='newtonAdmin'),
                    url(r'^login/$', views.show_login_view),
                    url(r'^login/post/$', views.post_login),
                    url(r'^logout/$', views.logout),
                    url(r'^kyc/$', views.kyc_admin, name='kyc_admin'),
                    url(r'^kyc/detail/', views.kyc_detail, name='kyc_detail'),
                    url(r'^kyc/update/', views.kyc_update, name='update_kycinfo'),
                    url(r'^kyc/send-email/', views.kyc_send_email),
                    url(r'^kyc/export-csv/', views.kyc_export_csv),
                    url(r'^blog/$', views.blog_admin, name='blog_admin'),
)