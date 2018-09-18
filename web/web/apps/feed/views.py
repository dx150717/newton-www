from django.shortcuts import render
import PyRSS2Gen
from django.conf import settings
import datetime
from django.http import HttpResponse
from zinnia.views.entries import EntryDetail
from zinnia.managers import CHINESE,ENGLISH,PUBLISHED,TYPE_BLOG,TYPE_ANNOUNCEMENT

def feed_latest(request):
	entry = EntryDetail()
	entries = entry.get_queryset().filter(language=CHINESE, status=PUBLISHED).order_by('-creation_date')[:20]
	for entry in entries:
		if entry.entry_type == TYPE_ANNOUNCEMENT:
			url = entry.get_absolute_url().replace('/blog/', '/announcement/')
			entry.urls = url
		else:
			entry.urls = entry.get_absolute_url()
	items = []
	for entry in entries:
		link = "%s%s" % (settings.BASE_URL, entry.urls)
		enclosure = None
		if entry.image:
			enclosure = PyRSS2Gen.Enclosure(entry.image.url, 1024, 'image/jpeg')
		item = PyRSS2Gen.RSSItem(title=entry.title,
								link=link,
								guid=PyRSS2Gen.Guid(link),
								enclosure=enclosure,
								pubDate=entry.creation_date)
		items.append(item)
	rss = PyRSS2Gen.RSS2(
		title='newtonproject.org',
		link="%s/feed/" % settings.BASE_URL,
		description="newtonproject",
		lastBuildDate=datetime.datetime.now(),
		language='zh-CN',
		docs='%s/about/' % settings.BASE_URL,
		items=items)
	rss.rss_attrs['xmlns:atom'] = 'http://www.w3.org/2005/Atom'
	xml = rss.to_xml(encoding='UTF-8')
	return HttpResponse(xml, mimetype = 'application/rss+xml;charset=utf-8')
