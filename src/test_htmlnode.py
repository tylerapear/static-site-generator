import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
    
    def test_eq(self):
        node1 = ParentNode("h1", [LeafNode(None, "This is a "), LeafNode("b", "bold"), LeafNode(None, " text")], props={"color": "red"})
        node2 = ParentNode("h1", [LeafNode(None, "This is a "), LeafNode("b", "bold"), LeafNode(None, " text")], props={"color": "red"})
        self.assertEqual(node1, node2)
    
    def test_repr(self):
        childNode = HTMLNode()
        props = {"color": "red"}
        node = HTMLNode(tag="h1", value="testval", children=[childNode], props=props)
        self.assertEqual(
            repr(node), 
            "HTMLNode(tag='h1', value='testval', children=[HTMLNode(tag='None', value='None', children=None, props=None)], props={'color': 'red'})"
        )
        
        
    ### Test LeafNode
        
    def test_leaf_init(self):
        node = LeafNode("p", "Hello World!", {"color": "red"})
        self.assertEqual(
            repr(node),
            "LeafNode(tag='p', value='Hello World!', props={'color': 'red'})"
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
        
    ### Test ParentNode
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiple_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = LeafNode("span", "child_node2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span>child_node2</span></div>",
        )
        
    def test_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
            
    def test_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
            


if __name__ == "__main__":
    unittest.main()