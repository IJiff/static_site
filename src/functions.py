from htmlnode import *
import re




def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        new_node_text = "";
        i = 0
        while i < len(text):
            if text[i] in delimiter:
                new_nodes.append(TextNode(new_node_text, TextType.TEXT))
                new_node_text = ""
                for j in range(len(delimiter)):
                    i += 1
                while text[i] not in delimiter:
                    new_node_text += text[i]
                    i += 1
                new_nodes.append(TextNode(new_node_text, text_type))
                for j in range(len(delimiter)):
                    i += 1
                new_node_text = ""
            else:
                new_node_text += text[i]
                i += 1
        if len(new_node_text) != 0:
            new_nodes.append(TextNode(new_node_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)     #The * is followed by ?, so that it isn't greedy


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        markdown_images = extract_markdown_images(node.text)
        modified_text = re.sub(r"!\[.*?\]\(.*?\)", "![]()", node.text)
        node_text_buffer = ""
        i = 0
        while i < len(modified_text):
            if modified_text[i] != '!':
                node_text_buffer += modified_text[i]
                i += 1
            else:
                if modified_text[i:i+5] == "![]()":
                    if len(node_text_buffer) != 0:
                        new_nodes.append(TextNode(node_text_buffer, TextType.TEXT))
                        node_text_buffer = ""
                    markdown_tuple = markdown_images.pop(0)
                    new_nodes.append(TextNode(markdown_tuple[0], TextType.IMAGE, markdown_tuple[1]))
                    i += 5
                else:
                    node_text_buffer += modified_text[i]
                    i += 1
        if len(node_text_buffer) != 0:
            new_nodes.append(TextNode(node_text_buffer, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        markdown_links = extract_markdown_links(node.text)
        modified_text = re.sub(r"\[.*?\]\(.*?\)", "[]()", node.text)
        node_text_buffer = ""
        i = 0
        while i < len(modified_text):
            if modified_text[i] != '[':
                node_text_buffer += modified_text[i]
                i += 1
            else:
                if modified_text[i:i+4] == "[]()":
                    if len(node_text_buffer) != 0:
                        new_nodes.append(TextNode(node_text_buffer, TextType.TEXT))
                        node_text_buffer = ""
                    markdown_tuple = markdown_links.pop(0)
                    new_nodes.append(TextNode(markdown_tuple[0], TextType.LINK, markdown_tuple[1]))
                    i += 4
                else:
                    node_text_buffer += modified_text[i]
                    i += 1
        if len(node_text_buffer) != 0:
            new_nodes.append(TextNode(node_text_buffer, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    fixed_blocks = []
    for block in blocks:
        fixed_blocks.append(block.strip())
    final_blocks = []
    for block in fixed_blocks:
        if block != '\n' and block != '':
            final_blocks.append(block)
    return final_blocks





