import unittest

from htmlnode import *
from functions import *


class TestExtractMarkdownImages(unittest.TestCase):
    def one_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def multiple_images(self):
        matches = extract_markdown_images("This is the ![first image](image1.yeet), this is the ![second image](image2.yeet), and this is the ![third image](image3.yeet)")
        self.assertListEqual([("first image", "image1.yeet"), ("second image", "image2.yeet"), ("third image", "image3.yeet")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def one_link(self):
        matches = extract_markdown_images("This text here has [some text that links to something else](externalLink.yeet)")
        self.assertListEqual([("some text that links to something else", "externalLink.yeet")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_beginning(self):
        node = TextNode("![This is text with an image at the beginning](beginning.yeet), so maybe the function will have a problem (who knows?)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an image at the beginning", TextType.IMAGE, "beginning.yeet"),
            TextNode(", so maybe the function will have a problem (who knows?)", TextType.TEXT),
        ], new_nodes)


class TestSplitnodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_beginning(self):
        node = TextNode("[This is text with an image at the beginning](beginning.yeet), so maybe the function will have a problem (who knows?)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with an image at the beginning", TextType.LINK, "beginning.yeet"),
            TextNode(", so maybe the function will have a problem (who knows?)", TextType.TEXT),
        ], new_nodes)


class TestTextToTextnodes(unittest.TestCase):
    def one_of_everything(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def the_monster(self):
        nodes = text_to_textnodes("**This text** is starting with bold, followed by _this_ ![image of a yeet](yeetskeet.yeet). `Then, we have a code block` _immediately followed by italics_ [and a link](link.yeet), to be ultimately **finished with some more bold text")
        self.assertListEqual(
            [
                TextNode("This text", TextType.BOLD),
                TextNode(" is starting with bold, folloed by ", TextType, TEXT),
                TextNode("this", TextType.ITALIC),
                TextNode("image of a yeet", TextType.IMAGE, "yeetskeet.yeet"),
                TextNode(". ", TextType.TEXT),
                TextNode("Then, we have a code block", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("immediately followed by italics", TextType.Italic),
                TextNode(" ", TextType.TEXT),
                TextNode("and a link", TextType.LINK, "link.yeet"),
                TextNode(", to be ultimately ", TextType.TEXT),
                TextNode("finished with some more bold text", TextType.BOLD),
            ],
            nodes
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_extra_whitespace(self):
        md = """
This is going to be _some random text_, but it will have



**a lot of**




newlines between




`each section`
Heck yeah baby
I think I goofed in my function lol
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is going to be _some random text_, but it will have",
                "**a lot of**",
                "newlines between",
                "`each section`\nHeck yeah baby\nI think I goofed in my function lol"
            ]
        )
