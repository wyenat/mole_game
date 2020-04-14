class Tree:
    """Builds the tree of the explored states
    """

    def __init__(self, state: str, parent=None):
        """
        :param state: state at root of the tree
        :type state: str
        """
        self.parent = parent
        self.state = state
        self.children = []

    def add_children(self, children):
        for child in children:
            self.children.append(Tree(state=child, parent=self))

    def pretty