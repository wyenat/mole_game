#!/usr/bin/env python3
from sim.board import Board
from ui.interface import GraphicalUserInterface

def main():
    # Opens a rando
    board = Board(5)
    board.map_import("maps/map_5x5.map")
    GraphicalUserInterface(board)



if __name__ == "__main__":
    main()
