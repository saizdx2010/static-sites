class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        list = []
        for prop in self.props:
            list.append(f'{prop}="{self.props[prop]}"')

        return " " + " ".join(list)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError('Value is None')
        if self.tag == None:
            return self.value
        if self.props == None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            props_value = self.props_to_html()
            return f'<{self.tag} {props_value}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Node does not have tag value")

        if self.children == None:
            raise ValueError("Parent Node does not contain children element")

        children_value = ''
        for child in self.children:
            children_value += child.to_html()

        if self.props == None:
            return f'<{self.tag}>{children_value}</{self.tag}>'

        return f'<{self.tag}{self.props_to_html()}>{children_value}</{self.tag}>'
