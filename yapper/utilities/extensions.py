from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension

try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs


LAZY_YT_PATTERN = '\[!lazyembed(\?(.*))?\]\((.*)\)'
LAZY_YT_PLACEHOLDER = u'<div class="lazyYT" data-youtube-id="%s" ' \
    'data-ratio="16:9">Loading video...</div>'


class LazyYoutubePattern(Pattern):

    """Enables lazy loading of youtube youtub videos."""

    def __init__(self, md):
        super(LazyYoutubePattern, self).__init__(LAZY_YT_PATTERN)
        self.md = md

    def handleMatch(self, m):
        url = m.group(4)
        (max_width, max_height) = self.__parse_params(m.group(3))
        urlparts = url.split('?v=')
        if len(urlparts) != 2:
            raise Exception('Invalid Youtube URL.')
        html = LAZY_YT_PLACEHOLDER % urlparts[1]
        return self.md.htmlStash.store(html)

    def __parse_params(self, query_string):
        if not query_string:
            return None, None

        query_params = parse_qs(query_string)
        return (self.__get_query_param(query_params, 'max_width'),
                self.__get_query_param(query_params, 'max_height'))

    @staticmethod
    def __get_query_param(query_params, name):
        if name in query_params:
            return int(query_params[name][0])
        else:
            return None


class LazyYoutubeExtension(Extension):

    """
    Parses a youtube URL in markdown and renders that as an empty div
    with data-* attributes to be used by lazyyt.js.
    """

    def __init__(self):
        super(LazyYoutubeExtension, self).__init__()

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add(
            'lazyyoutubeembed', LazyYoutubePattern(md), '_begin')
