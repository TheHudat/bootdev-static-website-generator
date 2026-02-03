import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_three_children(self):
        child_node1 = LeafNode("a", "child1")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("c", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><a>child1</a><b>child2</b><c>child3</c></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_two_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        child_node1 = ParentNode("span", [grandchild_node1])
        grandchild_node2 = LeafNode("c", "grandchild2")
        child_node2 = ParentNode("r", [grandchild_node2])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b></span><r><c>grandchild2</c></r></div>",
        )
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)
        