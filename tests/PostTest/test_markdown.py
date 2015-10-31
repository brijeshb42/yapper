import unittest
from yapper.utilities.md import create_post_from_md


class TestTextConversion(unittest.TestCase):

    def test_md_conversion(self):
        post = """# Hello
What is this?

*hah* [Another](http://another.com)

**intexturl** http://google.com

    from os import path
    print(os.abspath(__name__))
"""
        html = create_post_from_md(post)
        assert "<h1>Hello</h1>" in html
        assert ('<a class="link-external" '
                'href="http://another.com"'
                ' target="_blank">Another</a>') in html
        assert ('<a class="link-external" '
                'href="http://google.com" '
                'target="_blank">http://goo'
                'gle.com</a>') in html
