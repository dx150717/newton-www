"""Models for Zinnia"""
from django_comments.moderation import moderator

from events.models.entry import Entry
from events.models.author import Author
from events.models.category import Category

from events.signals import connect_entry_signals
from events.signals import connect_discussion_signals

from events.moderator import EntryCommentModerator

# Here we import the Zinnia's Model classes
# to register the Models at the loading, not
# when the Zinnia's URLs are parsed. Issue #161.
__all__ = [Entry.__name__,
           Author.__name__,
           Category.__name__]

# Register the comment moderator on Entry
if Entry not in moderator._registry:
    moderator.register(Entry, EntryCommentModerator)

# Connect the signals
connect_entry_signals()
connect_discussion_signals()
