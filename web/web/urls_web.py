from django.conf.urls import patterns, include, url
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.contrib import admin
from django.views.static import serve as serve_static
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, RedirectView

from welcome import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'welcome.views.show_home_view'),
                       url(r'^home/', 'welcome.views.show_home_view'),
                       url(r'^technology/', 'welcome.views.show_tech_view'),
                       url(r'^protocol/', 'welcome.views.show_protocol_view'),
                       url(r'^newpay/', 'welcome.views.show_newpay_view'),
                       url(r'^community/', 'welcome.views.show_community_view'),
                       url(r'^economy/', 'welcome.views.show_economy_view'),
                       url(r'^team/', 'welcome.views.show_team_view'),
                       url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
                       url(r'^announcement/$', views.AnnouncementView.as_view()),
                       url(r'^announcements/(?P<entry_sub_type>\d{1})/$', views.AnnouncementSubView.as_view()),
                       url(r'^announcement/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)', views.AnnouncementDetailView.as_view()),
                       url(r'^about/', 'welcome.views.show_about_view'),
                       url(r'^joinus/', 'welcome.views.show_joinus_view'),
                       url(r'^contact/', 'welcome.views.show_contact_view'),
                       url(r'^roadmap/', 'welcome.views.show_roadmap_view'),
                       url(r'^partner/', 'welcome.views.show_partner_view'),
                       url(r'^foundation/', 'welcome.views.show_foundation_view'),
                       url(r'^copyright/', 'welcome.views.show_copyright_view'),
                       url(r'^terms-of-use/', 'welcome.views.show_terms_of_use_view'),
                       url(r'^privacy/', 'welcome.views.show_privacy_view'),
                       url(r'^legal/', 'welcome.views.show_legal_view'),
                       url(r'^mediakit/', 'welcome.views.show_mediakit_view'),
                       url(r'^tinymce/zinnia/', include('zinnia_tinymce.urls')),
                       url(r'^tinymce/', include('tinymce.urls')),
                       url(r'^comments/', include('django_comments.urls')),
                       url(r'^subscribe/',include('subscription.urls')),
                       url(r'^press/',include('press.urls')),
                       url(r'^faq/',include('faq.urls')),
                       url(r'^ishuman/',include('ishuman.urls')),
                       url(r'^help/',include('help.urls')),
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
