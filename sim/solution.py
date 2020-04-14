from sim.board import Board
class Solution:
    def __init__(self, board : Board):
        self.board = board
        self.possible_actions = {}
        self.states_encountered = {}

    def stop_condition(self):
        return len(self.board.moles) == 0

    def cost_action(self, x, y):
        return 1 + self.board.mole_clicked(x, y, False, False)

    def total_value(self):
        return len(self.board.moles)

    def bellman(self):
        i = 0
        self.states_encountered[str(self.board.moles)] = len(self.board.moles)
        while not self.stop_condition() and i<1000:
            self.board.sort_moles()
            for mole in self.board.moles:
                mole_y = mole // self.board.N 
                mole_x = mole % self.board.N
                self.possible_actions[mole] = self.cost_action(mole_x, mole_y)
            finished_round = False
            already = False
            while not finished_round:
                if len(self.possible_actions):
                    print("No more actions, revert")
                    self.board.history.undo()
                    break
                best = min(self.possible_actions, key=self.possible_actions.get)
                mole_y = best // self.board.N 
                mole_x = best % self.board.N
                self.board.mole_clicked(mole_x, mole_y, False, True)
                if already:
                    print(f"choose {self.board.moles} instead")
                if str(self.board.moles) in self.states_encountered:
                    print(f"{self.board.moles} already encountered !")
                    undone = self.board.history.undo()
                    already = True
                    if undone is not None:
                        self.board.mole_clicked(undone[0], undone[1], False)

                    self.possible_actions.pop(best)
                    finished_round = False
                else:
                    self.states_encountered[str(self.board.moles)] = len(self.board.moles)
                    already = False
                    finished_round = True
                    self.possible_actions = {}
            i += 1
        print(self.states_encountered)
        print(i, len(self.states_encountered))