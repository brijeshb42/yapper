from urlparse import urlparse

from markdown import markdown
from markdown.extensions.codehilite import CodeHilite
import bleach

from config import Config


def externallify_url(attrs, new=False):
    """Open external urls in new tab.

    This is a callback function used by bleach.linkify().
    Add attribute target=_blank in all the urls that are not
    from the domains in Config.DOMAINS
    """
    p = urlparse(attrs['href'])
    if p.netloc not in Config.DOMAINS:
        # attrs['rel'] = 'nofollow'
        attrs['target'] = '_blank'
        attrs['class'] = 'external'
    else:
        attrs.pop('target', None)
    return attrs


def dont_linkify_urls(attrs, new=False):
    """Prevent file extensions to convert to links.

    This is a callback function used by bleach.linkify().
    Prevent strings ending with substrings in `file_exts` to be
    converted to links unless it starts with http or https.
    """
    file_exts = ('.py', '.md', '.sh')
    txt = attrs['_text']
    if txt.startswith(('http:', 'https:')):
        return attrs
    if txt.endswith(file_exts):
        return None
    return attrs


def create_post_from_md(body):
    """Parse markdown and linkify urls."""
    # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
    #                'em', 'li', 'i', 'ol', 'pre', 'strong', 'ul', 'h1',
    #                'h2', 'h3', 'p', 'span']
    return bleach.linkify(
        markdown(
            body,
            output_format='html5',
            extensions=['codehilite(linenums=True)']
        ),
        callbacks=[externallify_url, dont_linkify_urls],
        skip_pre=True
    )
    """
    Previous version of the function
    return bleach.linkify(
        markdown(
            bleach.clean(
                body,
                tags=allowed_tags
            ),
            output_format='html5',
            extensions=['codehilite(linenums=True)']
        ),
        callbacks=[externallify_url, dont_linkify_urls],
        skip_pre=True
    )"""
