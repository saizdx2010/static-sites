class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, another_node):
        if self.text == another_node.text and self.text_type == another_node.text_type and self.url == another_node.url:
            return True
        else:
            return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
