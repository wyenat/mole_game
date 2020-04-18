class Tree:
    """Builds the tree of the explored states
    """

    def __init__(
        self, state: str, action:int, value:int, size_of_board:int, parent=None, states=set()
    ):
        """
        :param state: state at root of the tree
        :type state: str
        :param action: Action required from parent state to get to this state
        :type action: int 
        :param value: value in the Bellman algorithm
        :type value: int
        :param size_of_board: Size of the board
        :type size_of_board: int
        :param Parent: Parent of the current state
        :type Parent: Tree, optional
        :param states: All states reaches by this tree
        :type states: set
        """
        self.parent = parent
        self.state = state
        self.size_of_board = size_of_board
        self.children = list()
        self.states = states
        self.value = value
        self.action = action
        self.depth = 0 if parent is None else parent.depth + 1

    def add_children(self, child, value:int, action:int): 
        """ Add a child to the tree
        :param child: Child to add
        :type child: Tree
        :param action: Action required to get to the child
        :type action: int
        :param value: value in the bellman algorithm
        :type value: int 
        """
        child.sort()
        if str(child) not in self.states:
            # Add equivalent states to the States already reaches
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

    def pretty_print(self) -> str:
        """ Return the tree without equivalent states """
        if self.children == []:
            return f"{self.state, self.action}"
        string = f"{self.state, self.action}"
        for child in self.children:
            string += f"\n {'  |' * (1+self.depth)} {child.pretty_print()}"
        return string

    def extensive_print(self) -> str:
        """ Return a string of the tree with the equivalent states """
        if self.children == []:
            return f"{self.state, self.action}"
        state = [int(i) for i in self.state[1:-1].split(",")]
        string = f"{self.rot_and_sym(self.size_of_board, state)}"
        for child in self.children:
            string += f"\n {'  |' * (1+self.depth)} {child.extensive_print()}"
        return string

    def print_parents(self) -> str:
        """ Return the str of the actions required to get to this state"""
        if self.parent is None:
            return f"Moles clicked in order:"
        return (
            self.parent.print_parents()
            + f"\n{(self.action // self.size_of_board, self.action % self.size_of_board)}"
        )
 
    def get_actions(self):
        """ Return a list of the actions required to get to this state"""
        if self.parent is None:
            return []
        return self.parent.get_actions() + [self.action]

    def __hash__(self):
        return hash(self.state)

    @staticmethod
    def rot_and_sym(size_of_board :int, current_state) -> list:
        """ Find the states that are equal to the current states through rotation and symetries

        :param size_of_board: Size of the board
        :type size_of_board: int
        :param current_tree: Current tree
        :type current_tree: Tree
        :return: Equivalent states
        :rtype: list
        """

        def rotate(state: list) -> list:
            """ Rotate 90 degrees 
            :param state: positions of the moles
            :type state:"""
            rotated = []
            for mole in state:
                mole_y = mole // size_of_board
                mole_x = mole % size_of_board
                rotate_mole = size_of_board * (size_of_board - 1 - mole_x) + mole_y
                rotated.append(rotate_mole)
            rotated.sort()
            return rotated

        def symetry(state, axis : str):
            """ Symetry of axis
            :param axis: axis wanted
            :type axis: str
            """
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

        # Generate equivalent states by rotation
        rot0 = current_state
        rot0.sort()
        rot90 = rotate(rot0)
        rot180 = rotate(rot90)
        rot270 = rotate(rot180)
        rot = [rot0, rot90, rot180, rot270]

        # Generate equivalent states by symetry 
        sym_x = symetry(current_state, "x")
        sym_y = symetry(current_state, "x")

        # Generate equivalent states by rotation of the symetries
        sym_x90 = rotate(sym_x)
        sym_x180 = rotate(sym_x90)
        sym_x270 = rotate(sym_x180)
        sym_y90 = rotate(sym_y)
        sym_y180 = rotate(sym_y90)
        sym_y270 = rotate(sym_y180)
        sym = [sym_x, sym_x90, sym_x180, sym_x270, sym_y, sym_y90, sym_y180, sym_y270]
        rotnsym = []

        # Assert only unique states are added
        for state in rot + sym:
            str_state = str(state)
            if str_state not in rotnsym:
                rotnsym.append(str_state)
        return rotnsym
