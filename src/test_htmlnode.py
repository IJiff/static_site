import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(repr(node), "HTMLNode(p, This is a paragraph, None, None)")
        new_node = HTMLNode("h1", None, [HTMLNode(), HTMLNode("p")], {"href": "www.yourmom.com", "id": "paragraph"})
        self.assertEqual(repr(new_node), "HTMLNode(h1, None, [HTMLNode(None, None, None, None), HTMLNode(p, None, None, None)], {'href': 'www.yourmom.com', 'id': 'paragraph'})")

    def test_props_to_html(self):
        node = HTMLNode('p', "Some words", None, dict({"href": "www.yourmom.com"}))
        self.assertEqual(node.props_to_html(), " href=www.yourmom.com")
        new_node = HTMLNode(None, None, None, dict({"id": "Nothing", "href": "www.mydad.com", "class": "thing"}))
        self.assertEqual(new_node.props_to_html(), " id=Nothing href=www.mydad.com class=thing")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a link", {"href": "www.Rickrolled.gov"})
        self.assertEqual(node.to_html(), "<a href=www.Rickrolled.gov>This is a link</a>")
        
