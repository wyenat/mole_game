import os
from sim.mole import Mole


class Board:
    """ Mode, length=16, height=16l of the board """

    def __init__(self, N: int):
        """Builds the board and places the moles

        :param N: Size of the N*N board
        :type N: int
        """
        self.N = N
        self.moles = []

    def map_export(self, name: str, directory: str = "maps/"):
        """Export the board as a .map file in the map folder

        :param name: Name of the file
        :type name: str
        :param directory: directory of the file to save, defaults to "../maps/"
        :type directory: str, optional
        """
        complete_path = os.path.join(directory, name)
        with open(complete_path, "w") as map:
            map.write(f"{self.N}\n")
            for mole in self.moles:
                map.write(f"{mole} ")

    def map_import(self, path: str):
        """Import a .map file as a Board

        :param path: Path of the file
        :type path: str
        """
        if not os.path.exists(path):
            raise RuntimeError("Path not valid !")
        with open(path, "r") as map:
            read = map.readlines()
        self.N = int(read[0])
        for mole in read[1].split(" ")[:-1]:
            position = int(mole)
            self.moles.append(position)

    def add_mole(self, x, y):
        position = self.N * y + x
        self.moles.append(position)

    def get_size(self):
        return self.N
    
    def around_moles(self, position):
        """ returns the cases around the position 
        """
        neighbors = [position]
        if position % self.N != 0:
            neighbors.append(position - 1)
        if position % self.N != self.N - 1 :
            neighbors.append(position + 1)
        if position // self.N != 0:
            neighbors.append(position - self.N )
        if position // self.N != self.N + 1:
            neighbors.append(position + self.N)
        return neighbors

    def mole_clicked(self, x, y, is_quick):
        position = self.N * y + x
        if is_quick:
            # Quick edit : the game is not on
            mole = position
            if mole in self.moles:
                self.moles.remove(mole)
            else:
                self.moles.append(mole)
        else:
            # Touching a mole changes its neighbors
            neighbors = self.around_moles(position)
            for neighbor in neighbors:
                if neighbor in self.moles:
                    self.moles.remove(neighbor)
                else:
                    self.moles.append(neighbor)
        # Check if finished
        if self.moles == []:
            return True
        return False
    