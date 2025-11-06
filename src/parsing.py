from textnode import TextType, TextNode

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
