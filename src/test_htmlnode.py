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


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "urmom.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "urmom.com")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "urmom.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "urmom.com")
        self.assertEqual(html_node.props["alt"], "This is an image node")


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, answer)

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, answer)

    def test_italic(self):
        node = TextNode("This is text with _two_ different _italic_ words in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        answer = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("two", TextType.ITALIC),
            TextNode(" different ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" words in it", TextType.TEXT),
        ]

    def test_multiple(self):
        node = TextNode("This is text with **many** different _styles_ of `words` in it, but **we're** only _looking_ for **the bold words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        answer = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("many", TextType.BOLD),
            TextNode(" different _styles_ of `words` in it, but ", TextType.TEXT),
            TextNode("we're", TextType.BOLD),
            TextNode(" only _looking_ for ", TextType.TEXT),
            TextNode("the bold words", TextType.BOLD),
        ]
