import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter, extract_markdown_links, 
    extract_markdown_images, split_nodes_image, split_nodes_links,
    text_to_textnodes
    )


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

    def test_split_images_leading_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_single_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_back_to_back(self):
        node = TextNode(
            "This is text with double ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with double ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_space(self):
        node = TextNode(
            "This is text with double ![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with double ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_leading_link(self):
        node = TextNode(
            "[link](https://www.google.com) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_single_link(self):
        node = TextNode(
            "[link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_back_to_back(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_space(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_splits_no_markdown(self):
        node = TextNode("This is only text", TextType.TEXT)
        image_split_node = split_nodes_image([node])
        link_split_node = split_nodes_links([node])
        self.assertEqual([TextNode("This is only text", TextType.TEXT)], image_split_node)
        self.assertEqual([TextNode("This is only text", TextType.TEXT)], link_split_node)
        
    def test_text_to_textnode_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
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
            new_nodes,
        )

    def test_text_to_textnode_none(self):
        text = "This is just text"
        new_nodes = text_to_textnodes(text)
        self.assertEqual([TextNode("This is just text", TextType.TEXT)], new_nodes)
    
    def test_text_to_textnode_two(self):
        text = "This is **text** with an _italic_ word"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
