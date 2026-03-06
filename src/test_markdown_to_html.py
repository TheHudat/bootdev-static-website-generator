import unittest

from htmlnode import LeafNode
from markdown_to_html import (
    markdown_to_html_node,
    text_to_children, 
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_text_to_children(self):
        text = "This is another paragraph with _italic_ text and `code` here"
        child_nodes = text_to_children(text)
        solution = (
            '[LeafNode(TAG=None, VALUE="This is another paragraph with ", '
            'PROPS=()), LeafNode(TAG=i, VALUE="italic", PROPS=()), '
            'LeafNode(TAG=None, VALUE=" text and ", PROPS=()), '
            'LeafNode(TAG=code, VALUE="code", PROPS=()), '
            'LeafNode(TAG=None, VALUE=" here", PROPS=())]'
        )
        self.assertEqual(child_nodes.__repr__(), solution)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# heading 1

## heading 2

#### heading 4
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>heading 1</h1><h2>heading 2</h2><h4>heading 4</h4></div>",
        )
    
    def test_unordered_list(self):
        md = """
- list item 1
- list item 2
- list item 3 with _italic_ 
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>list item 1</li><li>list item 2</li><li>list item 3 with <i>italic</i></li></ul></div>",
        )
    
    def test_ordered_list(self):
        md = """
1. list item 1 with **bold**
2. list item 2
3. list item 3 with _italic_ 
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>list item 1 with <b>bold</b></li><li>list item 2</li><li>list item 3 with <i>italic</i></li></ol></div>",
        )

    def test_blockquote(self):
        md = """
> this is a quote
>with multiple lines
> including **bold** _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a quote with multiple lines including <b>bold</b> <i>italic</i></blockquote></div>",
        )
    