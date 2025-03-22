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
        

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_parents(self):
        child = LeafNode(None, "child")
        child1 = LeafNode("i", "child1")
        parent = ParentNode("div", [child, child1])
        child2 = LeafNode(None, "child2")
        child3 = LeafNode("b", "child3")
        parent1 = ParentNode("p", [child2, child3])
        final_parent = ParentNode("header", [parent, parent1])
        self.assertEqual(final_parent.to_html(), "<header><div>child<i>child1</i></div><p>child2<b>child3</b></p></header>")
