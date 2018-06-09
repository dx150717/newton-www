from django.conf.urls import patterns, include, url
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.contrib import admin
from django.views.static import serve as serve_static
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, RedirectView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', RedirectView.as_view(url='/newtonadmin/')),
                       url(r'^newtonadmin/',include('newtonadmin.urls')),
                       url(r'^ishuman/',include('ishuman.urls')),
                       # admin
                       url(r'^admin/tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'welcome.views.show_404_page'
handler500 = 'welcome.views.show_500_page'

urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', never_cache(serve_static),
                                {'document_root': '%s/static' % (settings.PROJECT_ROOT), 'show_indexes': True}))
urlpatterns += patterns('', url(r'^filestorage/(?P<path>.*)$', never_cache(serve_static),
                                {'document_root': '%s' % (settings.PROJECT_ROOT), 'show_indexes': True}))
