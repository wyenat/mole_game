#!/usr/bin/env python3
from sim.board import Board
from sim.solution import Solution
from ui.interface import GraphicalUserInterface
from time import clock


def main():
    # Create a map
    board = Board(3)

    # Optional : pre load a map
    board.map_import("maps/map_3x3.map")
    
    # Start the graphical interface
    GraphicalUserInterface(board)


if __name__ == "__main__":
    main()
