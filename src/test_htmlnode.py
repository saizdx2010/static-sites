
import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node1 = HTMLNode('<h1>', 'Hello World',)
        node2 = HTMLNode('<p>', 'This is a paragraph')
        node3 = HTMLNode(tag='<img>', props={'href': 'hola.img.com', 'alt': 'hola image alt'})
        print(node3.props_to_html())


if __name__ == "__main__":
    unittest.main()
