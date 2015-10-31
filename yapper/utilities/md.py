from urlparse import urlparse

from markdown import markdown
from pyembed.markdown import PyEmbedMarkdown
import bleach

from .extensions import LazyYoutubeExtension

from config import Config


def externallify_url(attrs, new=False):
    """Open external urls in new tab.

    This is a callback function used by bleach.linkify().
    Add attribute target=_blank in all the urls that are not
    from the domains in Config.DOMAINS
    """
    p = urlparse(attrs['href'])
    if p.netloc.lower() not in Config.DOMAINS:
        # attrs['rel'] = 'nofollow'
        attrs['target'] = '_blank'
        attrs['class'] = 'link-external'
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
    if txt.startswith(('http://', 'https://')):
        return attrs
    if txt.endswith(file_exts):
        return None
    return attrs


def create_post_from_md(body):
    """Parse markdown and linkify urls."""
    # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
    #                 'em', 'li', 'i', 'ol', 'pre', 'strong', 'ul', 'h1',
    #                 'h2', 'h3', 'p', 'span']
    no_link_text = markdown(
        body,
        output_format='html5',
        extensions=[
            'codehilite(linenums=True)',
            PyEmbedMarkdown(),
            LazyYoutubeExtension()
        ]
    )
    return bleach.linkify(
        no_link_text,
        callbacks=[externallify_url, dont_linkify_urls],
        skip_pre=True
    )
