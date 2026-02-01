class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        prop_string = ''
        for key, value in self.props.items():
            prop_string = prop_string + f' {key}="{value}"'
        return prop_string

    def __repr__(self):
        prop_string = self.props_to_html()
        return f'HTMLNode(TAG={self.tag}, VALUE="{self.value}", CHILDREN={self.children}, PROPS=({prop_string}))'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        prop_string = self.props_to_html()
        return f'LeafNode(TAG={self.tag}, VALUE="{self.value}", PROPS=({prop_string}))'
