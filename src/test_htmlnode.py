import unittest

from htmlnode import HTMLNode

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
    
    def test_print(self):
        self.maxDiff = None
        solution = (
        'HTMLNode(TAG=h1, VALUE="test value text", '
        'CHILDREN=(HTMLNode(TAG=a, VALUE="child_node1", PROPS=() '
        'HTMLNode(TAG=b, VALUE="child_node2", PROPS=() ), '
        'PROPS=( href="https://www.google.com" prop2="prop2 stuff"))'
        )
        self.assertEqual(self.test_node.__repr__(), solution)
    
    def test_values(self):
        node = HTMLNode("div", "value text")
        self.assertEqual(node.tag,  "div")
        self.assertEqual(node.value, "value text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        