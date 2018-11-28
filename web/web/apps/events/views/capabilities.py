"""Views for Zinnia capabilities"""
from django.contrib.sites.models import Site
from django.views.generic.base import TemplateView

from events.settings import PROTOCOL
from events.settings import COPYRIGHT
from events.settings import FEEDS_FORMAT


class CapabilityView(TemplateView):
    """
    Base view for the weblog capabilities.
    """

    def get_context_data(self, **kwargs):
        """
        Populate the context of the template
        with technical informations for building urls.
        """
        context = super(CapabilityView, self).get_context_data(**kwargs)
        context.update({'protocol': PROTOCOL,
                        'copyright': COPYRIGHT,
                        'feeds_format': FEEDS_FORMAT,
                        'site': Site.objects.get_current()})
        return context


class HumansTxt(CapabilityView):
    """
    http://humanstxt.org/
    """
    content_type = 'text/plain'
    template_name = 'events/humans.txt'


class RsdXml(CapabilityView):
    """
    http://en.wikipedia.org/wiki/Really_Simple_Discovery
    """
    content_type = 'application/rsd+xml'
    template_name = 'events/rsd.xml'


class WLWManifestXml(CapabilityView):
    """
    http://msdn.microsoft.com/en-us/library/bb463260.aspx
    """
    content_type = 'application/wlwmanifest+xml'
    template_name = 'events/wlwmanifest.xml'


class OpenSearchXml(CapabilityView):
    """
    http://www.opensearch.org/
    """
    content_type = 'application/opensearchdescription+xml'
    template_name = 'events/opensearch.xml'
