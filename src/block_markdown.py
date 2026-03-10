from enum import Enum
import re

from htmlnode import HTMLNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "oredered list"

def markdown_to_blocks(markdown):
    split_list = markdown.split("\n\n")
    markdown_lines = []
    for line in split_list:
        stripped_line = line.strip()
        if stripped_line != "":
            markdown_lines.append(stripped_line)
    return markdown_lines

def block_to_block_type(block):
    lines = block.split("\n")
    
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if re.match(r"> ?", block):
        for line in lines:
            if not re.match(r"> ?", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if re.match("- ", block):
        for line in lines:
            if not re.match("- ", line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def extract_title(markdown):
    return re.findall(r"(?<!#)# (.+)", markdown)[0]