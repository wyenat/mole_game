import os
from sim.history import History
from sim.tree import Tree
import copy


class Board:
    """ Class that specify the map """

    def __init__(self, N: int):
        """Builds the board and places the moles

        :param N: Size of the N*N board
        :type N: int
        """
        self.N = N
        self.moles = []
        self.history = History()
        self.tree = Tree(
            state=str(self.moles), action=None, value=0, size_of_board=self.get_size()
        )
        self.current = self.tree

    def sort_moles(self):
        """ Sort moles by position
        """
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
        self.moles = []
        if not os.path.exists(path):
            raise RuntimeError("Path not valid !")
        with open(path, "r") as map:
            read = map.readlines()
        self.N = int(read[0])
        for mole in read[1].split(" ")[:-1]:
            position = int(mole)
            self.moles.append(position)
        self.tree = Tree(
            state=str(self.moles),
            action=None,
            value=len(self.moles),
            size_of_board=self.get_size(),
        )
        self.current = self.tree

    def add_mole(self, x: int, y: int):
        """Add a mol in specified position

        :param x: coordinate x of the mole
        :type x: int
        :param y: coordinate y of the mole
        :type y: int
        """
        position = self.N * y + x
        self.moles.append(position)

    def get_size(self) -> int:
        """ Size of the map

        :return: Size of the map
        :rtype: int
        """
        return self.N

    def around_moles(self, position: int) -> list:
        """returns the cases around the position

        :param position: Position of the mole
        :type position: int
        :return: Cases around that moles
        :rtype: list
        """
        neighbors = [position]
        # Border cases
        # Left
        if position % self.N != 0:
            neighbors.append(position - 1)
        # Right
        if position % self.N < self.N - 1 and position < self.N ** 2:
            neighbors.append(position + 1)
        # Top
        if position // self.N != 0:
            neighbors.append(position - self.N)
        # Bottom
        if position + self.N < self.N ** 2:
            neighbors.append(position + self.N)
        return neighbors

    def mole_clicked(self, x: int, y: int, is_quick: bool, apply: bool = True, update_tree = False):
        """Callback function for when a mole is touched.

        :param x: position x of the mole
        :type x: int
        :param y: position y of the mole
        :type y: int
        :param is_quick: if quick edit of the map is enabled
        :type is_quick: bool
        :param apply: if the modification should be applied, defaults to True
        :type apply: bool, optional
        :return: if apply=True, returns a bool that confirms if the map is finished.
        Else, returns the difference in mole numbers
        :rtype: bool
        """
        # History Managed
        if apply and (x, y) != self.history.last:
            self.history.add_click(x, y)
        position = self.N * y + x
        if is_quick:
            # Quick edit : the game is not on
            mole = position
            if mole in self.moles:
                self.moles.remove(mole)
            else:
                self.moles.append(mole)
                # Check if finished
            if self.moles == []:
                return True
            return False
        else:
            # Touching a mole changes its neighbors
            neighbors = self.around_moles(position)
            added_value = len(self.moles)
            new = copy.deepcopy(self.moles)
            for neighbor in neighbors:
                if neighbor in self.moles:
                    added_value -= 1
                    new.remove(neighbor)
                else:
                    added_value += 1
                    new.append(neighbor)
        if apply:
            self.moles = new
        if update_tree:
            # Update the tree
            self.current.add_children(new, value=added_value, action=position)

        # Check if finished
        if self.moles == []:
            return True
        return False
