from sim.board import Board


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

    def bellman(self):
        """ Apply of the Bellman algorithm
        """
        i = 0
        self.states_encountered[str(self.board.moles)] = len(self.board.moles)
        while not self.stop_condition() and i < 2 ** ((self.board.N + 1) ** 2):
            print(f"\tEntering {i}")
            self.board.sort_moles()
            for mole in self.board.moles:
                mole_y = mole // self.board.N
                mole_x = mole % self.board.N
                self.possible_actions[mole] = self.cost_action(mole_x, mole_y)
            print(f"Possible actions = {self.possible_actions}")
            finished_round = False
            while not finished_round:
                if len(self.possible_actions) == 0:
                    print("No more actions, revert")
                    undone = self.board.history.undo()
                    if undone is not None:
                        print(f"BRANCH Reverting by clicking {undone[0], undone[1]}")
                        self.board.mole_clicked(undone[0], undone[1], False)
                    break
                best = min(self.possible_actions, key=self.possible_actions.get)
                print(f"best = {best}")
                mole_y = best // self.board.N
                mole_x = best % self.board.N
                self.board.mole_clicked(mole_x, mole_y, False, True)
                if str(self.board.moles) in self.states_encountered:
                    print(f"State = {self.board.moles} already encountered !")
                    undone = self.board.history.undo()
                    if undone is not None:
                        print(f"Reverting by clicking {undone[0], undone[1]}")
                        self.board.mole_clicked(undone[0], undone[1], False)
                    self.possible_actions.pop(best)
                    finished_round = False

                else:
                    self.states_encountered[str(self.board.moles)] = len(
                        self.board.moles
                    )
                    finished_round = True
                    self.possible_actions = {}
            i += 1
        print(i, len(self.states_encountered))
