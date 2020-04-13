class History:
    """ Allow the usage of history """
    def __init__(self):
        self.history = []
        self.deleted = []

    def undo(self):
        """ Undo the previous click
        """
        undone = None
        if self.history != []:
            undone = self.history.pop()
            self.deleted.append(undone)
        return undone


    def next(self):
        """ Redo the previous undone click 
        """
        forward = None
        if self.deleted != []:
            forward = self.deleted.pop()
            self.history.append(forward)
        return forward

    def new_map(self):
        self.forward = []
        self.history = []

    def add_click(self, x, y):
        """ Add an entry in the history
        """
        self.deleted = []
        self.history.append((x,y))