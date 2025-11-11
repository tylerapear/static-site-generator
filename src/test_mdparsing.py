import unittest

from mdparsing import *
from textnode import TextNode, TextType

class TestMDParsing(unittest.TestCase):
    
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
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_image_first(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is cool, and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is cool, and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_non_plain(self):
        node = TextNode(
            "this is code",
            TextType.CODE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_link_first(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) is cool, and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is cool, and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_link_non_plain(self):
        node = TextNode(
            "this is code",
            TextType.CODE,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )
        
        
class TestMDToHTML(unittest.TestCase):
    def test_text_to_textnodes(self):
        self.assertEqual(
            text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"),
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
        
    def test_text_to_html_nodes(self):
        self.maxDiff = None
        text = "This is **a bold** _italic_ `codely` line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_html_nodes(text),
            [
                LeafNode(None, "This is "),
                LeafNode("b", "a bold"),
                LeafNode(None, " "),
                LeafNode("i", "italic"),
                LeafNode(None, " "),
                LeafNode("code", "codely"),
                LeafNode(None, " line with an "),
                LeafNode("img", "", {"src": "https://i.imgur.com/fJRm4Vk.jpeg", "alt": "obi wan image"}),
                LeafNode(None, " and a "),
                LeafNode("a", "link", {"href": "https://boot.dev"}),
            ]
        )
        
    def test_markdown_to_blocks(self):
        md = """   
        
        
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_type_heading(self):
        block1 = "# a heading"
        block2 = "###### another heading"
        block3 = ".# not a heading"
        self.assertEqual(block_to_block_type(block1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block3), BlockType.NORMAL)
        
    def test_block_type_code(self):
        block1 = "``` code ```"
        block2 = "```notcode``"
        block3 = "``notcode```"
        self.assertEqual(block_to_block_type(block1), BlockType.CODE)
        self.assertEqual(block_to_block_type(block2), BlockType.NORMAL)
        self.assertEqual(block_to_block_type(block3), BlockType.NORMAL)
        
    def test_block_type_quote(self):
        block1 = ">quote"
        block2 = "> quote"
        block3 = "um> not quote"
        self.assertEqual(block_to_block_type(block1), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block2), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block3), BlockType.NORMAL)
        
    def test_block_type_unordered_list(self):
        block1 = "- unordered list"
        block2 = """- unordered
- list"""
        block3 = """- Not
. a list"""
        self.assertEqual(block_to_block_type(block1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(block2), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(block3), BlockType.NORMAL)
        
    def test_block_type_ordered_list(self):
        block1 = "1. ordered list"
        block2 = """1. ordered
2. list"""
        block3 = """1. Not
- a list"""
        self.assertEqual(block_to_block_type(block1), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block2), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block3), BlockType.NORMAL)
    
    
    def test_block_to_html_heading(self):
        self.maxDiff = None
        block1 = "#This is just a heading1"
        block3 = "###This is just a **bold** heading3"
        block6 = "######This is just a heading6"
        block7 = "#######This is just a heading6"
        htmlnode1 = block_to_html_heading(block1)
        htmlnode3 = block_to_html_heading(block3)
        htmlnode6 = block_to_html_heading(block6)
        htmlnode7 = block_to_html_heading(block7)
        self.assertEqual(
            htmlnode1,
            ParentNode("h1", [LeafNode(None, "This is just a heading1")])
        )
        self.assertEqual(
            htmlnode3,
            ParentNode("h3", [
                LeafNode(None, "This is just a "),
                LeafNode("b", "bold"),
                LeafNode(None, " heading3")
            ])
        )
        self.assertEqual(
            htmlnode6,
            ParentNode("h6", [LeafNode(None, "This is just a heading6")])
        )
        self.assertEqual(
            htmlnode7,
            ParentNode("h6", [LeafNode(None, "#This is just a heading6")])
        )
        
    def test_block_to_html_code(self):
        block = "```print('this **is** code')```"
        htmlnode = block_to_html_code(block)
        self.assertEqual(
            htmlnode,
            ParentNode("pre", [LeafNode("code", "print('this **is** code')")])
        )
        
    def test_block_to_html_quote(self):
        block = ">This is a quote"
        block2 = ">This is a **bold** quote"
        htmlnode = block_to_html_quote(block)
        htmlnode2 = block_to_html_quote(block2)
        self.assertEqual(
            htmlnode,
            ParentNode("blockquote", [
                LeafNode(None, "This is a quote")
            ])
        )
        self.assertEqual(
            htmlnode2,
            ParentNode("blockquote", [
                LeafNode(None, "This is a "),
                LeafNode("b", "bold"),
                LeafNode(None, " quote")
            ])
        )
        
    def test_block_to_html_unordered_list(self):
        self.maxDiff = None
        block = """- item 1
- item _uh_ 2
- item 3"""
        htmlnode = block_to_html_list(block, "-")
        self.assertEqual(
            htmlnode,
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "item 1")]),
                ParentNode("li", [
                    LeafNode(None, "item "),
                    LeafNode("i", "uh"),
                    LeafNode(None, " 2")
                ]),
                ParentNode("li", [LeafNode(None, "item 3")])
            ])
        )
        
    def test_block_to_html_ordered_list(self):
        self.maxDiff = None
        block = """. item 1
. item _uh_ 2
. item 3"""
        htmlnode = block_to_html_list(block, ".")
        self.assertEqual(
            htmlnode,
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "item 1")]),
                ParentNode("li", [
                    LeafNode(None, "item "),
                    LeafNode("i", "uh"),
                    LeafNode(None, " 2")
                ]),
                ParentNode("li", [LeafNode(None, "item 3")])
            ])
        )
        
    def test_block_to_html_normal(self):
        block = "This **is** just a _little_ text"
        htmlnode = block_to_html_normal(block)
        self.assertEqual(
            htmlnode,
            ParentNode("p", [
                LeafNode(None, "This "),
                LeafNode("b", "is"),
                LeafNode(None, " just a "),
                LeafNode("i", "little"),
                LeafNode(None, " text")
            ])
        )