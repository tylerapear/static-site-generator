import unittest

from textnode import TextNode, TextType, text_node_to_html_node, text_nodes_to_html_nodes
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node = TextNode("This is a text node1", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertEqual(
            'TextNode("This is a text node", bold, https://www.google.com)', repr(node)
        )
        
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"}
        )
        
    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
        
class TestTextNodesToHTMLNode(unittest.TestCase):
    def test_text_nodes(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        node3 = TextNode("This is bold", TextType.BOLD)
        html_nodes = text_nodes_to_html_nodes([node, node2, node3])
        html_reprs = [repr(node) for node in html_nodes]
        expected = [
            repr(LeafNode(None, "This is a text node")),
            repr(LeafNode("img", "", {"src": "https://www.boot.dev", "alt": "This is an image"})),
            repr(LeafNode("b", "This is bold"))
        ]
        self.assertEqual(repr(html_nodes[0]), "LeafNode(tag='None', value='This is a text node', props=None)")
        self.assertEqual(repr(html_nodes[1]), "LeafNode(tag='img', value='', props={'src': 'https://www.boot.dev', 'alt': 'This is an image'})")
        self.assertEqual(repr(html_nodes[2]), "LeafNode(tag='b', value='This is bold', props=None)")
        
if __name__ == "__main__":
    unittest.main()