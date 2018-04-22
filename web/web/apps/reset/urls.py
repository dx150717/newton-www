from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.show_repassword_view),
                    url(r'^edit_password/', views.show_edit_password_view),
)