"""Views for Zinnia sitemap"""
from django.views.generic import TemplateView

from events.models.entry import Entry
from events.models.author import Author
from events.models.category import Category


class Sitemap(TemplateView):
    """
    Sitemap view of the Weblog.
    """
    template_name = 'events/sitemap.html'

    def get_context_data(self, **kwargs):
        """
        Populate the context of the template
        with all published entries and all the categories.
        """
        context = super(Sitemap, self).get_context_data(**kwargs)
        context.update(
            {'entries': Entry.published.all(),
             'categories': Category.published.all(),
             'authors': Author.published.all()}
        )
        return context
