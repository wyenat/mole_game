#!/usr/bin/env python3
from sim.board import Board
from sim.solution import Solution
from ui.interface import GraphicalUserInterface

def main():
    # Opens a rando
    board = Board(5)
    board.map_import("maps/map_3x3.map")
    solution = Solution(board)
    solution.bellman()
    GraphicalUserInterface(board)



if __name__ == "__main__":
    main()
