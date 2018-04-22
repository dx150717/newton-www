from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.show_register_view, name="index"),
                    url(r'^postemail/', views.postemail, name="postemail"),
                    url(r'^verify/', views.show_verify_view, name="verify"),
                    url(r'^editpassword/', views.show_editpassword_view, name="editpassword"),
                    url(r'^postpassword/', views.postpassword, name="postpassword"),
)