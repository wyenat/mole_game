#!/usr/bin/env python3
from sim.board import Board
from sim.solution import Solution
from ui.interface import GraphicalUserInterface


def main():
    board = Board(5)
    board.map_import("maps/map_4x4.map")
    solution = Solution(board)
    solution.bellman()
    print(board.tree.pretty_print())
    #GraphicalUserInterface(board)


if __name__ == "__main__":
    main()
