import unittest

from block_markdown import (
    BlockType, 
    block_to_block_type,
    markdown_to_blocks
) 

class TestBlockMarkdown(unittest.TestCase):
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

    def test_markdown_to_blocks_three_new_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here"
            ],
        )
    
    def test_markdown_to_blocks_four_new_lines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here"
            ],
        )

    def test_block_to_block_type_heading(self):
        heading1 = "# heading number 1"
        heading2 = "### heading number 2"
        self.assertEqual(block_to_block_type(heading1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading2), BlockType.HEADING)
    
    def test_block_to_block_type_non_leading(self):
        heading = "text block with ## inside"
        quote = "text line >sldkjhh"
        self.assertEqual(block_to_block_type(heading), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(quote), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_numbered_list(self):
        correct_list = "1. thing 1\n2. thing 2\n3. thing 3"
        wrong_list = "1. thing 1\n6. thing 2\n3. thing 3"
        self.assertEqual(block_to_block_type(correct_list), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(wrong_list), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_unordered_list(self):
        correct_list = "- thing 1\n- thing 2\n- thing 3"
        wrong_list = "- thing 1\nthing 2\n- thing 3"
        self.assertEqual(block_to_block_type(correct_list), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(wrong_list), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_code(self):
        code = """
```
code stuff
with multiple lines
def a function
```
"""
        self.assertEqual(block_to_block_type(code.strip()), BlockType.CODE)
    
    def test_block_to_block_type_code(self):
        quote = """
> this is a quote
>with multiple
> lines
"""
        self.assertEqual(block_to_block_type(quote.strip()), BlockType.QUOTE)
