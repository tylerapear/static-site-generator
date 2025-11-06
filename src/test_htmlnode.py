import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode(tag="h1", value="testval")
        with self.assertRaises(NotImplementedError):
            node.to_html()
            
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html(self):
        node = HTMLNode(props={"color": "red", "font": "arial"})
        self.assertEqual(node.props_to_html(), ' color="red" font="arial"')
    
    def test_repr(self):
        childNode = HTMLNode()
        props = {"color": "red"}
        node = HTMLNode(tag="h1", value="testval", children=[childNode], props=props)
        self.assertEqual(
            repr(node), 
            "HTMLNode(tag=h1, value=testval, children=[HTMLNode(tag=None, value=None, children=None, props=None)], props={'color': 'red'})"
        )
        
    ### Test LeafNode
        
    def test_leaf_init(self):
        node = LeafNode("p", "Hello World!", {"color": "red"})
        self.assertEqual(
            repr(node),
            "LeafNode(tag=p, value=Hello World!, props={'color': 'red'})"
        )
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello World!")
        self.assertEqual(node.to_html(), "Hello World!")
        
    def test_leaf_to_html_props(self):
        node = LeafNode("p", "Hello World!", {"color": "red", "font": "arial"})
        self.assertEqual(node.props_to_html(), ' color="red" font="arial"')


if __name__ == "__main__":
    unittest.main()