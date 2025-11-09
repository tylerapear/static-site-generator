

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        html = ""
        for key in self.props:
            html += f' {key}="{self.props[key]}"'
        return html
    
    def __eq__(self, other):
        if (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        ):
            return True
    
    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"
        
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag='{self.tag}', value='{self.value}', props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("invalid ParentNode: node has no children")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag='{self.tag}', children={self.children}, props={self.props})"