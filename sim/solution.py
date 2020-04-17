from sim.tree import Tree
import time
import copy


class Solution:
    """ Solution of the problem, using the Bellman equation
    to find a dynamic programing solution to this problem.
    """

    def __init__(self, board):
        """
        :param board: board on which the solution will be applied
        :type board: Board
        """
        self.board = board
        self.possible_actions = set()
        self.states_encountered = {}
        self.max_depth = float("inf")
        self.stop = False
        self.reverting_length = {}
        self.best_solution = None

    def build_branch(self):
        self.board.sort_moles()
        for mole in self.board.moles:
            mole_y = mole // self.board.N
            mole_x = mole % self.board.N
            self.board.mole_clicked(mole_x, mole_y, False, False, update_tree=True)

        for child in self.board.current.children:
            if child.depth < self.get_max_depth():
                self.possible_actions.add(child)

    def stop_reached(self):
        return self.stop

    def set_max_depth(self, max):
        self.max_depth = max

    def get_max_depth(self):
        return self.max_depth

    def apply_action(self, action):
        mole_y = action // self.board.N
        mole_x = action % self.board.N
        self.board.mole_clicked(mole_x, mole_y, False, True, update_tree=False)

    def get_to(self, tree):
        # Reverting from current to root
        actions_to_remove = self.board.current.get_actions()
        for action in actions_to_remove:
            self.apply_action(action)
        # Going from root to tree
        actions_to_do = tree.get_actions()
        for action in actions_to_do:
            self.apply_action(action)
        self.board.current = tree

    def determine_best(self):
        # ENDING CONDITIONS
        if self.board.current.state == "[]":
            print(f"PATH FOUND ! \n {self.board.current.print_parents()}")
            self.best_solution = self.board.current
            # self.set_max_depth(self.board.current.depth)
            for possible in self.possible_actions.copy():
                if possible.depth >= self.get_max_depth():
                    self.possible_actions.remove(possible)
            if len(self.possible_actions) == 0:
                return self.board.current
        best = min(self.possible_actions)
        best.value = float("inf")
        self.possible_actions.remove(best)
        return best

    def bellman(self):
        """ Apply of the Bellman algorithm
        """
        i = 0
        while not self.stop_reached():
            self.build_branch()
            if len(self.possible_actions) == 0:
                self.stop = True
            else:
                best = self.determine_best()
                self.get_to(best)
                i += 1
        return (
            self.best_solution.print_parents()
            if self.best_solution is not None
            else "There is no solutions"
        )

    def tree_to_here(self):
        print(f"entering for {self.board.current.state}")
        if self.board.current.state == "[]":
            positions = range(self.board.get_size())
        else:
            positions = self.board.moles
        for position in positions:
            neighbours = self.board.around_moles(position)
            for neigh in neighbours:
                mole_y = neigh // self.board.N
                mole_x = neigh % self.board.N
                if neigh not in self.board.moles:
                    self.board.mole_clicked(mole_x, mole_y, False, False, True)
        for child in self.board.current.children:
            save = copy.deepcopy(self.board.current)
            self.board.current = child
            mole_y = child.action // self.board.N
            mole_x = child.action % self.board.N
            self.board.mole_clicked(mole_x, mole_y, False, True, True)
            self.tree_to_here()
            self.board.current = save
