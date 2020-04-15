from sim.board import Board
from sim.tree import Tree


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
            self.board.mole_clicked(mole_x, mole_y, False, False)
        print(
            f"Finished building branches, {self.board.current.state} has for children {[i.state for i in self.board.current.children]}"
        )

    def determine_best(self):
        finished = False
        while not finished:
            if self.board.current.children is not None:
                best = min(self.board.current.children)
                print(f"best = {best.state, best.value, best.action}")
                mole_y = best.action // self.board.N
                mole_x = best.action % self.board.N
                # Apply best
                self.board.current = best
                self.board.mole_clicked(mole_x, mole_y, False, True)
                finished = True
            else:
                print("Reverting !")
                self.board.current.value = float("inf")
                self.board.current = self.board.current.parent
                undone = self.board.history.undo()
                if undone is not None:
                    print(f"BRANCH Reverting by clicking {undone[0], undone[1]}")
                    self.board.mole_clicked(undone[0], undone[1], False)
                    self.board.current = self.board.current.parent

    def bellman(self):
        """ Apply of the Bellman algorithm
        """
        i = 0
        while not self.stop_condition() and i < 10:
            print(f"\tEntering {i}")
            self.build_branch()
            print("Choosing best branch")
            self.determine_best()
            i += 1
        print(f"Met {len(self.board.tree.states)} different states")
