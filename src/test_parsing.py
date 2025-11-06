import unittest

from parsing import split_nodes_delimiter
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    
    def test_single_code_line(self):
        node = TextNode("This is text with a `code block` and a word", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[0],
            TextNode("This is text with a ", TextType.PLAIN)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[1],
            TextNode("code block", TextType.CODE)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[2],
            TextNode(" and a word", TextType.PLAIN)
        )
        
    def test_multiple_code_in_line(self):
        node = TextNode("This is text with a `code block` and another `code block2` and a word", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[0],
            TextNode("This is text with a ", TextType.PLAIN)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[1],
            TextNode("code block", TextType.CODE)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[2],
            TextNode(" and another ", TextType.PLAIN)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[3],
            TextNode("code block2", TextType.CODE)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[4],
            TextNode(" and a word", TextType.PLAIN)
        )
        
    def test_single_bold_line(self):
        node = TextNode("This is text with a **bold block** and a word", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD)[0],
            TextNode("This is text with a ", TextType.PLAIN)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD)[1],
            TextNode("bold block", TextType.BOLD)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD)[2],
            TextNode(" and a word", TextType.PLAIN)
        )
        
    def test_line_beginning_with_code(self):
        node = TextNode("`some code` and some `more code`", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[0],
            TextNode("some code", TextType.CODE)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[1],
            TextNode(" and some ", TextType.PLAIN)
        )
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[2],
            TextNode("more code", TextType.CODE)
        )
        
    def test_no_closing_delimiter(self):
        node = TextNode("`some code` and some `more code", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
            
    def test_no_delimiter(self):
        node = TextNode("*some code* and some *more code*", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE)[0],
            TextNode("*some code* and some *more code*", TextType.PLAIN)
        )
        
    def test_non_plain_text_type(self):
        node = TextNode("some code **and** some more code", TextType.CODE)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD)[0],
            TextNode("some code **and** some more code", TextType.CODE)
        )