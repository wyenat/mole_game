import os
from sim.history import History

class Board:
    """ Mode, length=16, height=16l of the board """

    def __init__(self, N: int):
        """Builds the board and places the moles

        :param N: Size of the N*N board
        :type N: int
        """
        self.N = N
        self.moles = []
        self.history = History()

    def sort_moles(self):
        self.moles.sort()

    def map_export(self, name: str, directory: str = "maps/"):
        """Export the board as a .map file in the map folder

        :param name: Name of the file
        :type name: str
        :param directory: directory of the file to save, defaults to "../maps/"
        :type directory: str, optional
        """
        self.sort_moles()
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
        self.history.new_map()
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
        if position % self.N < self.N - 1 and position < self.N ** 2:
            neighbors.append(position + 1)
        if position // self.N != 0:
            neighbors.append(position - self.N )
        if position + self.N < self.N ** 2 :
            neighbors.append(position + self.N)
        return neighbors

    def mole_clicked(self, x, y, is_quick, apply=True):
        if apply and (x,y) != self.history.last:
            self.history.add_click(x, y)
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
            added_value = len(self.moles)
            for neighbor in neighbors:
                if neighbor in self.moles:
                    added_value -= 1
                    if apply:
                        self.moles.remove(neighbor)
                else:
                    added_value += 1
                    if apply:
                        self.moles.append(neighbor)
        # If not applied, just returns the added_value
        if not apply:
            return added_value
        # Check if finished
        if self.moles == []:
            return True
        return False
    