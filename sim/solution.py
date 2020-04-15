from sim.board import Board
from sim.tree import Tree
import time

class Solution:
    """ Solution of the problem, using the Bellman equation
    to find a dynamic programing solution to this problem.
    """

    def __init__(self, board: Board):
        """
        :param board: board on which the solution will be applied
        :type board: Board
        """
        self.board = board
        self.possible_actions = {}
        self.states_encountered = {}
        self.max_depth = float("inf")
        self.stop = False

    def stop_condition(self) -> bool:
        """Stopping condition of the Bellman algorithm

        :return: number of moles is 0
        :rtype: bool
        """
        return len(self.board.moles) == 0

    def cost_action(self, x: int, y: int) -> int:
        """Cost of the action for the next step of Bellman algorithm

        :param x: Position x of the action
        :type x: int
        :param y: Position y of the action
        :type y: int
        :return: Cost of the action
        :rtype: int
        """
        return 1 + self.board.mole_clicked(x, y, False, False)

    def total_value(self) -> int:
        """ Total number of moles

        :return: Number of moles
        :rtype: int
        """
        return len(self.board.moles)

    def build_branch(self):
        self.board.sort_moles()
        for mole in self.board.moles:
            mole_y = mole // self.board.N
            mole_x = mole % self.board.N
            self.board.mole_clicked(mole_x, mole_y, False, False, update_tree=True)
        #print(
        #    f"Finished building branches, {self.board.current.state} has for children {[i.state for i in self.board.current.children]}"
        #)

    def stop_reached(self):
        return self.stop

    def set_max_depth(self, max):
        self.max_depth = max 
    
    def get_max_depth(self):
        return self.max_depth

    def determine_best(self):
        finished = False
        while not finished:
            if self.board.current.state == "[]":
                print(f"PATH FOUND ! \n {self.board.current.print_parents()}")
                self.set_max_depth(self.board.current.depth)
                undone = self.board.history.undo()
            valid_children = [child for child in self.board.current.children if child.value != float("inf")]
            if valid_children != [] and self.board.current.depth < self.get_max_depth():
                #print(f"Choosing best in {[(child.state, child.value) for child in self.board.current.children]}")
                best = min(self.board.current.children)
                mole_y = best.action // self.board.N
                mole_x = best.action % self.board.N
                # Apply best
                self.board.current = best
                self.board.mole_clicked(mole_x, mole_y, False, True, update_tree=False)
                finished = True
            else:
                if self.board.current.parent is None:
                    print("WE ARRIVED HOME.")
                    self.stop = True
                    finished = True
                #print("Reverting !")
                #print(f"history is {self.board.history.history}, reverted is {self.board.history.deleted}")
                self.board.current.value = float("inf")
                undone = self.board.current.parent.action
                if undone is not None:
                    undone_x = undone % self.board.get_size()
                    undone_y = undone // self.board.get_size()
                    self.board.current = self.board.current.parent
                    self.board.mole_clicked(undone_x, undone_y, False, update_tree=False)
                else:
                    print(f"Can't revert ! State is {self.board.current.state}, path is {self.board.current.print_parents()}")
                    self.stop = True
                    finished = True

    def bellman(self):
        """ Apply of the Bellman algorithm
        """
        i = 0
        while not self.stop_reached() and i < 6000:
            print(f"\tEntering {i}")
            self.build_branch()
            self.determine_best()
            i += 1
        
        print(f"Met {len(self.board.tree.states)} different states in {i} turns")
