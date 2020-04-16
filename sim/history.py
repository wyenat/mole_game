import os.path


class History:
    """ Allow the usage of history """

    def __init__(self):
        # History of actions
        self.history = []
        # History of actions undone
        self.deleted = []
        # Last entry to the history
        self.last = None

    def undo(self):
        """ Undo the previous click
        """
        undone = None
        if self.history != []:
            undone = self.history.pop()
            self.deleted.append(undone)
        self.last = undone
        return undone

    def next(self):
        """ Redo the previous undone click
        """
        forward = None
        if self.deleted != []:
            forward = self.deleted.pop()
            self.history.append(forward)
        self.last = forward
        return forward

    def new_map(self):
        """Clear the history
        """
        self.forward = []
        self.history = []

    def add_click(self, x: int, y: int):
        """Add an entry in the history

        :param x: Position x of the action stored in the history
        :type x: int
        :param y: Position y of the action stored in the history
        :type y: int
        """
        self.deleted = []
        self.history.append((x, y))

    def log(self, directory, name):
        complete_path = os.path.join(directory, name)
        with open(complete_path, "w") as log:
            log.write(f"History of moles clicked :")
            log.write(f"{self.history}")
