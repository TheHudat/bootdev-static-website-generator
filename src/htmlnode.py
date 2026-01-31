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
        child_string = ''
        if self.children:
            for child in self.children:
                child_string += f'HTMLNode(TAG={child.tag}, VALUE="{child.value}", PROPS=({child.props_to_html()}) '
        return f'HTMLNode(TAG={self.tag}, VALUE="{self.value}", CHILDREN=({child_string}), PROPS=({prop_string}))'