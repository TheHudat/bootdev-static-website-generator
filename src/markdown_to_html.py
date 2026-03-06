import re

from block_markdown import (
    markdown_to_blocks, 
    block_to_block_type,
    BlockType
)
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in markdown_blocks:
        block_node = block_to_html_node(block)
        block_nodes.append(block_node)
    return ParentNode("div", block_nodes)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    if block_type is BlockType.PARAGRAPH:
        new_lines_removed = block.replace("\n", " ")
        return ParentNode("p", text_to_children(new_lines_removed))
    if block_type is BlockType.CODE:
        child = LeafNode(None, block.strip("`\n") + "\n")
        block_node = ParentNode("code", [child])
        return ParentNode("pre", [block_node])
    if block_type is BlockType.HEADING:
        prefix_split = block.split(" ", 1)
        header_number = len(prefix_split[0])
        return ParentNode(f"h{header_number}", text_to_children(prefix_split[1]))
    if block_type is BlockType.QUOTE:
        return blockquote_to_html_node(block)
    if block_type is BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type is BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

def text_to_children(text):
    text_node_list = text_to_textnodes(text)
    child_nodes = []
    for node in text_node_list:
        html_node = text_node_to_html_node(node)
        child_nodes.append(html_node)
    return child_nodes

def unordered_list_to_html_node(list_block):
    item_list = re.findall(r"- (.+)", list_block)
    children = []
    for item in item_list:
        item_node = ParentNode("li", text_to_children(item))
        children.append(item_node)
    return ParentNode("ul", children)

def ordered_list_to_html_node(list_block):
    item_list = re.findall(r"\d+\. (.+)", list_block)
    children = []
    for item in item_list:
        item_node = ParentNode("li", text_to_children(item))
        children.append(item_node)
    return ParentNode("ol", children)

def blockquote_to_html_node(block):
    text_list = re.findall(r"> ?(.+)", block)
    quote_text = ""
    i = 1
    for text in text_list:
        if i == 1:
            quote_text += text
        else:
            quote_text += f" {text}"
        i += 1
    return ParentNode("blockquote", text_to_children(quote_text))
