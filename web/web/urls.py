from django.conf.urls import patterns, include, url
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.contrib import admin
from django.views.static import serve as serve_static
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static

from welcome import views
from search import views as search_views


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'welcome.views.show_home_view'),
                       url(r'^home/', 'welcome.views.show_home_view'),
                       url(r'^technology/$', 'welcome.views.show_technology_view'),
                       url(r'^technology/basic-tech/', 'welcome.views.show_tech_view'),
                       url(r'^technology/hep/', 'welcome.views.show_protocol_view'),
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
                       url(r'^newfund/', 'welcome.views.show_foundation_view'),
                       url(r'^copyright/', 'welcome.views.show_copyright_view'),
                       url(r'^terms-of-use/', 'welcome.views.show_terms_of_use_view'),
                       url(r'^privacy/', 'welcome.views.show_privacy_view'),
                       url(r'^legal/', 'welcome.views.show_legal_view'),
                       url(r'^mediakit/', 'welcome.views.show_mediakit_view'),
                       url(r'^whitepaper/', 'welcome.views.show_whitepaper_view'),
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
                       url(r'^term-of-service/', 'welcome.views.show_term_of_service_view'),
                       url(r'^solutions/', 'welcome.views.show_scene_view'),
                       url(r'^sitemap/', 'welcome.views.show_sitemap_view'),
                       url(r'^feed/', 'feed.views.feed_latest'),
                       url(r'^newstatus/', 'welcome.views.show_newstatus_view'),
                       url(r'^dashboard/', 'welcome.views.show_dashboard_view'),
                       url(r'^business-proposal/', 'welcome.views.show_business_proposal_view'),
                       url(r'^join-partner/', 'welcome.views.show_join_partner_view'),
                       url(r'^community-voice/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)', views.CommunityVoiceDetailView.as_view()),
                       url(r'^community-voice/$', views.CommunityVoiceView.as_view()),
                       url(r'^search/', include('search.urls')),
                       url(r'^nep/', 'welcome.views.show_nep_view'),
                       # web push
                       url(r'^webpush/', include('webpush.urls')),
                       url(r'sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'welcome.views.show_404_page'
handler500 = 'welcome.views.show_500_page'

urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', never_cache(serve_static),
                                {'document_root': '%s/static' % (settings.PROJECT_ROOT), 'show_indexes': True}))
urlpatterns += patterns('', url(r'^filestorage/(?P<path>.*)$', never_cache(serve_static),
                                {'document_root': '%s' % (settings.PROJECT_ROOT), 'show_indexes': True}))
