from urlparse import urlparse

from markdown import markdown
from markdown.extensions.codehilite import CodeHilite
import bleach

from config import Config


def externallify_url(attrs, new=False):
    p = urlparse(attrs['href'])
    if p.netloc not in Config.DOMAINS:
        # attrs['rel'] = 'nofollow'
        attrs['target'] = '_blank'
        attrs['class'] = 'external'
    else:
        attrs.pop('target', None)
    return attrs


def dont_linkify_urls(attrs, new=False):
    file_exts = ('.py', '.md', '.sh')
    txt = attrs['_text']
    if txt.startswith(('http:', 'https:')):
        return attrs
    if txt.endswith(file_exts):
        return None
    return attrs


def create_post_from_md(body):
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'li', 'i', 'ol', 'pre', 'strong', 'ul', 'h1',
                    'h2', 'h3', 'p', 'span']
    return bleach.linkify(
        markdown(
            bleach.clean(
                body,
                tags=allowed_tags, strip=True
            ),
            output_format='html5',
            extensions=['codehilite(linenums=True)']
        ),
        callbacks=[externallify_url, dont_linkify_urls],
        skip_pre=True
    )
