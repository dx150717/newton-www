from django.conf.urls import patterns, include, url

urlpatterns = patterns('user.views',
    url(r'^$', 'user_view'),
    url(r'^(?P<user_id>[0-9]+)/$', 'user_view'),
    url(r'^edit/$', 'user_edit_profile_view'),
    url(r'^edit/profile/$', 'user_edit_profile_view'),
    url(r'^edit/profile/profile-submit/$', 'user_edit_profile_submit_view'),
    url(r'^edit/account/$', 'user_edit_account_view'),
)
