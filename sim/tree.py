class Tree:
    """Builds the tree of the explored states
    """

    def __init__(self, state: str, size_of_board, parent=None, states=[]):
        """
        :param state: state at root of the tree
        :type state: str
        """
        self.parent = parent
        self.state = state
        self.size_of_board = size_of_board
        self.children = []
        self.states = states
        self.depth = 0 if parent == None else parent.depth + 1

    def add_children(self, children):
        for child in children:
            if str(child) not in self.states:
                equivalents = self.rot_and_sym(
                    size_of_board=self.size_of_board, current_state=child
                )
                self.children.append(
                    Tree(
                        state=equivalents[0],
                        size_of_board=self.size_of_board,
                        parent=self,
                        states=self.states,
                    )
                )
                for equivalent in equivalents:
                    self.states.append(equivalent)
            else:
                self.children = None

    def pretty_print(self):
        if self.children is None:
            return f"{self.state}"
        if self.children == []:
            return f"{self.state}\n {'  |' * (1+self.depth)} ???"
        string = f"{self.state}"
        for child in self.children:
            string += f"\n {'  |' * (1+self.depth)} {child.pretty_print()}"
        return string

    @staticmethod
    def rot_and_sym(size_of_board, current_state) -> list:
        """ Find the states that are equal to the current states through rotation and symetries

        :return: Equivalent states
        :rtype: list
        """

        def rotate(state):
            rotated = []
            for mole in state:
                mole_y = mole // size_of_board
                mole_x = mole % size_of_board
                rotate_mole = size_of_board * (size_of_board - 1 - mole_x) + mole_y
                rotated.append(rotate_mole)
            rotated.sort()
            return rotated

        def symetry(state, axis):
            symetry = []
            for mole in state:
                mole_y = mole // size_of_board
                mole_x = mole % size_of_board
                if axis == "x":
                    symetry_mole = size_of_board * (size_of_board - 1 - mole_y) + mole_x
                elif axis == "y":
                    symetry_mole = size_of_board * mole_y + (size_of_board - 1 - mole_x)
                symetry.append(symetry_mole)
            symetry.sort()
            return symetry

        rot0 = current_state
        rot0.sort()
        rot90 = rotate(rot0)
        rot180 = rotate(rot90)
        rot270 = rotate(rot180)
        rot = [rot0, rot90, rot180, rot270]
        sym = [symetry(current_state, "x"), symetry(current_state, "y")]
        rotnsym = list(set([str(to_hash) for to_hash in rot + sym]))
        return rotnsym
