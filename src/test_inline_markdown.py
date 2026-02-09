import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images


class TestSplitNodes(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a ```code block``` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "```", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
            )
    
    def test_split_bold(self):
        node = TextNode("Front text **bolded text** back text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Front text ", TextType.TEXT),
                TextNode("bolded text", TextType.BOLD),
                TextNode(" back text", TextType.TEXT),
            ]
            )
        
    def test_split_no_delimiter(self):
        node = TextNode("Front text **bolded text** back text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Front text **bolded text** back text", TextType.TEXT)
            ]
            )
    
    def test_split_bold_double(self):
        node = TextNode("Front text **bolded text1** middle text **bolded text2** back text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Front text ", TextType.TEXT),
                TextNode("bolded text1", TextType.BOLD),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("bolded text2", TextType.BOLD),
                TextNode(" back text", TextType.TEXT),
            ]
            )
        
    def test_split_one_delimiter_error(self):
        node = TextNode("Front text **bolded text back text", TextType.TEXT)
        node2 = TextNode("Front text **bolded text1** middle text **bolded text2 back text", TextType.TEXT)
        node3 = TextNode("text **bolded text1** text **bolded text2** text **bold back text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node2], "**", TextType.BOLD)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node3], "**", TextType.BOLD)
    
    def test_split_nontext(self):
        node = TextNode("Front text **bolded text** back text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Front text **bolded text** back text", TextType.BOLD)
            ]
            )
    
    def test_split_node_list(self):
        node = TextNode("Front text **bolded text** back text", TextType.TEXT)
        node2 = TextNode("Front text2 **bolded text2** back text2", TextType.TEXT)
        node3 = TextNode("Front text _italic text_ back text", TextType.TEXT)
        node4 = TextNode("text type code", TextType.CODE)
        new_nodes = split_nodes_delimiter([node, node2, node3, node4], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Front text ", TextType.TEXT),
                TextNode("bolded text", TextType.BOLD),
                TextNode(" back text", TextType.TEXT),
                TextNode("Front text2 ", TextType.TEXT),
                TextNode("bolded text2", TextType.BOLD),
                TextNode(" back text2", TextType.TEXT),
                TextNode("Front text _italic text_ back text", TextType.TEXT),
                TextNode("text type code", TextType.CODE)      
            ]
            )
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![alt text](www.site.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("alt text", "www.site.com")], matches)
    
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_link_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)