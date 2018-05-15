from django.conf.urls import patterns, include, url

urlpatterns = patterns('logout.views',
                       url(r'^$', 'logout_view'),
)
