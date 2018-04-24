from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.show_login_view),
                    url(r'^post/', views.login_post, name="loginpost")
)