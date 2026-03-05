import re

from textnode import TextNode, TextType

def text_to_textnodes(text):
    start_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([start_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_links(new_nodes)
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) == 2 or (len(split_text) != 3 and len(split_text) % 3 != 2):
            raise Exception("Invalid Markdown Syntax: text contained a delimiter with no pair")
        for i in range(len(split_text)):
            if (i + 1) % 2 != 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        markdown_images = extract_markdown_images(node.text)
        if markdown_images == []:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for set in markdown_images:
            image_text = set[0]
            url = set[1]
            split_text = remaining_text.split(f"![{image_text}]({url})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image_text, TextType.IMAGE, url))
            remaining_text = split_text[1]
        if split_text[1] != "":
                new_nodes.append(TextNode(split_text[1], TextType.TEXT))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        markdown_links = extract_markdown_links(node.text)
        if markdown_links == []:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for set in markdown_links:
            link_text = set[0]
            url = set[1]
            split_text = remaining_text.split(f"[{link_text}]({url})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            remaining_text = split_text[1]
        if split_text[1] != "":
                new_nodes.append(TextNode(split_text[1], TextType.TEXT))
    return new_nodes

