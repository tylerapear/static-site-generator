import unittest

from htmlnode import HTMLNode

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
        print(node)
        self.assertEqual(
            repr(node), 
            "HTMLNode(tag=h1, value=testval, children=[HTMLNode(tag=None, value=None, children=None, props=None)], props={'color': 'red'})"
        )


if __name__ == "__main__":
    unittest.main()