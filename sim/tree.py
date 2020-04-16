class Tree:
    """Builds the tree of the explored states
    """

    def __init__(
        self, state: str, action, value, size_of_board, parent=None, states=set()
    ):
        """
        :param state: state at root of the tree
        :type state: str
        """
        self.parent = parent
        self.state = state
        self.size_of_board = size_of_board
        self.children = list()
        self.states = states
        self.value = value
        self.action = action
        self.depth = 0 if parent is None else parent.depth + 1

    def add_children(self, child, value, action):
        child.sort()
        if str(child) not in self.states:
            equivalents = self.rot_and_sym(
                size_of_board=self.size_of_board, current_state=child
            )
            tree = Tree(
                state=equivalents[0],
                value=value,
                action=action,
                size_of_board=self.size_of_board,
                parent=self,
                states=self.states,
            )
            self.children.append(tree)
            for equivalent in equivalents:
                self.states.add(str(equivalent))

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def pretty_print(self):
        if self.state == "[]":
            return f"[] --- Valid path !"
        if self.value == float("inf"):
            return f"{self.state, self.action}"
        if self.children == []:
            return f"{self.state, self.action}\n {'  |' * (1+self.depth)} ???"
        string = f"{self.state, self.action}"
        for child in self.children:
            string += f"\n {'  |' * (1+self.depth)} {child.pretty_print()}"
        return string

    def print_parents(self):
        if self.parent is None:
            return f"Moles clicked in order:"
        return (
            self.parent.print_parents()
            + f"\n{(self.action // self.size_of_board, self.action % self.size_of_board)}"
        )

    def get_actions(self):
        if self.parent is None:
            return []
        return self.parent.get_actions() + [self.action]

    def __hash__(self):
        return hash(self.state)

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
        rotnsym = []
        for state in rot + sym:
            str_state = str(state)
            if str_state not in rotnsym:
                rotnsym.append(str_state)
        return rotnsym
