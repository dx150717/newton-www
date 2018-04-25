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
                    url(r'^kyc/id-confirm/$', views.kyc_id_confirm),
                    url(r'^kyc/amount-confirm/$', views.kyc_amount_confirm),
                    url(r'^kyc/email-confirm/$', views.kyc_email_confirm),
                    url(r'^kyc/email-list/$', views.kyc_email_list),
                    url(r'^kyc/step-one/', views.kyc_step_one),
                    url(r'^kyc/step-two/', views.kyc_step_two),
                    url(r'^kyc/step-three/', views.kyc_step_three),
                    url(r'^kyc/update-id/', views.kyc_update_id),
                    url(r'^kyc/update-amount/', views.kyc_update_amount),
                    url(r'^kyc/update-email/', views.kyc_update_email),
                    url(r'^kyc/send-one-email/', views.kyc_send_one_email),
                    url(r'^kyc/send-email/', views.kyc_send_email),
                    url(r'^kyc/export-csv/', views.kyc_export_csv),
                    url(r'^blog/$', views.blog_admin),
)