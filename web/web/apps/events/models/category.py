"""Category model for Zinnia"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from mptt.managers import TreeManager

from events.managers import entries_published
from events.managers import EntryRelatedPublishedManager
from events.managers import CHINESE, ENGLISH, TYPE_ANNOUNCEMENT, TYPE_BLOG

@python_2_unicode_compatible
class Category(MPTTModel):
    """
    Simple model for categorizing entries.
    """
    LANGUAGE_CHOICES = (
        (CHINESE, _('zh_CN')),
        (ENGLISH, _('en'))
    )

    ENTRY_TYPE_CHOICES = (
        (TYPE_BLOG, _('Blog')),
        (TYPE_ANNOUNCEMENT, _('Announcement'))
    )

    title = models.CharField(
        _('title'), max_length=255)

    slug = models.SlugField(
        _('slug'), unique=True, max_length=255,
        help_text=_("Used to build the category's URL."))

    description = models.TextField(
        _('description'), blank=True)

    parent = TreeForeignKey(
        'self',
        related_name='children',
        null=True, blank=True,
        verbose_name=_('parent category'))

    language = models.IntegerField(
        _('language'),
        choices=LANGUAGE_CHOICES,default=ENGLISH,
        db_index=True, 
        help_text=_('Language')
    )

    entry_type = models.IntegerField(
        _('Entry type'),
        choices=ENTRY_TYPE_CHOICES,default=TYPE_BLOG,
        db_index=True,
        help_text=_('Entry type')
    )

    objects = TreeManager()
    published = EntryRelatedPublishedManager()

    def entries_published(self):
        """
        Returns category's published entries.
        """
        return entries_published(self.entries)

    @property
    def tree_path(self):
        """
        Returns category's tree path
        by concatening the slug of his ancestors.
        """
        if self.parent_id:
            return '/'.join(
                [ancestor.slug for ancestor in self.get_ancestors()] +
                [self.slug])
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        """
        Builds and returns the category's URL
        based on his tree path.
        """
        return ('events:category_detail', (self.tree_path,))

    def __str__(self):
        return self.title

    class Meta:
        """
        Category's meta informations.
        """
        app_label = 'events'
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        """
        Category MPTT's meta informations.
        """
        order_insertion_by = ['title']
