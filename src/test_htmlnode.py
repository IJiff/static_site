import unittest

from htmlnode import HTMLNode

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

