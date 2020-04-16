#!/usr/bin/env python3
from sim.board import Board
from sim.solution import Solution
from ui.interface import GraphicalUserInterface
from time import clock


def main():
    board = Board(5)
    # board.map_import("maps/map_3x3.map")
    # solution = Solution(board)
    # top = clock()
    # solution.bellman()
    # print(f"Done in {clock() - top} s")
    # print(f"Met {len(board.tree.states)} different states")
    GraphicalUserInterface(board)


if __name__ == "__main__":
    main()
