import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    child_node1 = HTMLNode('a', 'child_node1')
    child_node2 = HTMLNode('b', 'child_node2')
    test_props = {
        "href": "https://www.google.com",
        "prop2": "prop2 stuff"
    }
    test_node = HTMLNode("h1", "test value text", [child_node1, child_node2], test_props)
    
    def test_props_to_html(self):
        solution = ' href="https://www.google.com" prop2="prop2 stuff"'
        self.assertEqual(self.test_node.props_to_html(), solution)
    
    def test_htmlnode_print(self):
        self.maxDiff = None
        solution = (
        'HTMLNode(TAG=h1, VALUE="test value text", '
        'CHILDREN=[HTMLNode(TAG=a, VALUE="child_node1", CHILDREN=None, PROPS=()), '
        'HTMLNode(TAG=b, VALUE="child_node2", CHILDREN=None, PROPS=())], '
        'PROPS=( href="https://www.google.com" prop2="prop2 stuff"))'
        )
        self.assertEqual(self.test_node.__repr__(), solution)
    
    def test_htmlnode_values(self):
        node = HTMLNode("div", "value text")
        self.assertEqual(node.tag,  "div")
        self.assertEqual(node.value, "value text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_blockquote(self):
        node = LeafNode("blockquote", "Hello, world!", {'href':'https://www.google.com'})
        self.assertEqual(node.to_html(), '<blockquote href="https://www.google.com">Hello, world!</blockquote>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, 'text here')
        self.assertEqual(node.to_html(), 'text here')

    def test_leaf_print(self):
        self.maxDiff = None
        test_props = {
        "href": "https://www.google.com",
        "prop2": "prop2 stuff"
        }
        node = LeafNode("h1", "test value text", test_props)
        solution = (
        'LeafNode(TAG=h1, VALUE="test value text", '
        'PROPS=( href="https://www.google.com" prop2="prop2 stuff"))'
        )
        self.assertEqual(node.__repr__(), solution)
        