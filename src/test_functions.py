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
