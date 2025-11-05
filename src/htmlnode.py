

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
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
            

def test():
    props = {
    "href": "https://www.google.com",
    "target": "_blank",
    }
    
    node = HTMLNode(props=props)
    print(node.props_to_html())
    
test()