import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("node text", TextType.IMAGE, "https://")
        node2 = TextNode("node text", TextType.IMAGE, "https://")
        self.assertEqual(node, node2)
    
    def test_noteq_urlnone(self):
        node = TextNode("I am a text node", TextType.CODE, "www.site.com")
        node2 = TextNode("I am a text node", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_noteq_texttype(self):
        node = TextNode("sample text", TextType.LINK)
        node2 = TextNode("sample text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_noteq_text(self):
        node = TextNode("I am text node text", TextType.LINK)
        node2 = TextNode("I am not text node text", TextType.LINK)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()