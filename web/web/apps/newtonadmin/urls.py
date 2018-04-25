from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.index),
                    url(r'^login/$', views.show_login_view),
                    url(r'^login/post/$', views.post_login),
                    url(r'^logout/$', views.logout),
                    url(r'^kyc/$', views.kyc_admin),
                    url(r'^kyc/step-one/', views.kyc_step_one),
                    url(r'^kyc/step-two/', views.kyc_step_two),
                    url(r'^kyc/step-three/', views.kyc_step_three),
                    url(r'^kyc/update/', views.kyc_update),
                    url(r'^kyc/send-one-email/', views.kyc_send_one_email),
                    url(r'^kyc/send-email/', views.kyc_send_email),
                    url(r'^kyc/export-csv/', views.kyc_export_csv),
                    url(r'^blog/$', views.blog_admin),
)