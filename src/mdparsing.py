import re
from enum import Enum

from textnode import TextType, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    NORMAL = "normal"
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        elements = node.text.split(delimiter)
        if len(elements) % 2 == 0:
            raise ValueError(f'Invalid node: no closing delimiter: "{delimiter}" in string: "{node.text}"')
        
        for i in range(len(elements)):
            if elements[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(elements[i], TextType.PLAIN))
            else:
                new_nodes.append(TextNode(elements[i], text_type))
        
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        text_parts = re.split(r"!\[.*?\]\(.*?\)", node.text)
        image_parts = extract_markdown_images(node.text)
        
        for i in range(len(image_parts)):
            text_part = text_parts.pop(0)
            if text_part != "":
                new_nodes.append(
                    TextNode(text_part, TextType.PLAIN)
                )
            new_nodes.append(
                TextNode(image_parts[i][0], TextType.IMAGE, image_parts[i][1])
            )
            
        for remaining in text_parts:
            if remaining != "":
                new_nodes.append(
                    TextNode(remaining, TextType.PLAIN)
                )
                
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        text_parts = re.split(r"\[.*?\]\(.*?\)", node.text)
        link_parts = extract_markdown_links(node.text)
        
        for i in range(len(link_parts)):
            text_part = text_parts.pop(0)
            if text_part != "":
                new_nodes.append(
                    TextNode(text_part, TextType.PLAIN)
                )
            new_nodes.append(
                TextNode(link_parts[i][0], TextType.LINK, link_parts[i][1])
            )
            
        for remaining in text_parts:
            if remaining != "":
                new_nodes.append(
                    TextNode(remaining, TextType.PLAIN)
                )
                
    return new_nodes

def text_to_textnodes(text):
    original_node = TextNode(text, TextType.PLAIN)
    return (
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_link(
                        split_nodes_image(
                            [original_node]    
                        )
                    ), "`", TextType.CODE
                ), "_", TextType.ITALIC
            ), "**", TextType.BOLD
        )
    )
    
def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    filtered_blocks = []
    for i in range(len(blocks)):
        if blocks[i] != "":
            filtered_blocks.append(blocks[i])
    return filtered_blocks

def block_to_block_type(block):
    if block[0] == "#":
        return BlockType.HEADING
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    if block[0] == ">":
        return BlockType.QUOTE
    
    lines = block.split("\n")
    blocktype = BlockType.NORMAL
    for line in lines:
        if line[:2] == "- ":
            blocktype = BlockType.UNORDERED_LIST
        else:
            blocktype = BlockType.NORMAL
            break
    if blocktype == BlockType.NORMAL:
        for line in lines:
            if line[:2] == ". ":
                blocktype = BlockType.ORDERED_LIST
            else:
                blocktype = BlockType.NORMAL
                break
   
    return blocktype
