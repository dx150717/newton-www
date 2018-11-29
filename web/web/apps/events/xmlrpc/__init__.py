"""XML-RPC methods for Zinnia"""


ZINNIA_XMLRPC_PINGBACK = [
    ('events.xmlrpc.pingback.pingback_ping',
     'pingback.ping'),
    ('events.xmlrpc.pingback.pingback_extensions_get_pingbacks',
     'pingback.extensions.getPingbacks')]

ZINNIA_XMLRPC_METAWEBLOG = [
    ('events.xmlrpc.metaweblog.get_users_blogs',
     'blogger.getUsersBlogs'),
    ('events.xmlrpc.metaweblog.get_user_info',
     'blogger.getUserInfo'),
    ('events.xmlrpc.metaweblog.delete_post',
     'blogger.deletePost'),
    ('events.xmlrpc.metaweblog.get_authors',
     'wp.getAuthors'),
    ('events.xmlrpc.metaweblog.get_tags',
     'wp.getTags'),
    ('events.xmlrpc.metaweblog.get_categories',
     'metaWeblog.getCategories'),
    ('events.xmlrpc.metaweblog.new_category',
     'wp.newCategory'),
    ('events.xmlrpc.metaweblog.get_recent_posts',
     'metaWeblog.getRecentPosts'),
    ('events.xmlrpc.metaweblog.get_post',
     'metaWeblog.getPost'),
    ('events.xmlrpc.metaweblog.new_post',
     'metaWeblog.newPost'),
    ('events.xmlrpc.metaweblog.edit_post',
     'metaWeblog.editPost'),
    ('events.xmlrpc.metaweblog.new_media_object',
     'metaWeblog.newMediaObject')]

ZINNIA_XMLRPC_METHODS = ZINNIA_XMLRPC_PINGBACK + ZINNIA_XMLRPC_METAWEBLOG
