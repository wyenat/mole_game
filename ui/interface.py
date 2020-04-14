from tkinter import *
from tkinter import filedialog
from sim.board import Board
from random import randint
import webbrowser

class GraphicalUserInterface:
    """ Graphical interface of the Mole game, allowing the game to be 
    played through a graphical interface 
    """

    def change_quick(self):
        """Enable or disable the quick edit mode
        """
        self.is_quick = not self.is_quick

    def show_help(self):
        """Show the help 
        """
        webbrowser.open_new(r'doc/Help.pdf')

    def import_map(self):
        """ Opens the file selector to select the map to load 
        """
        map_file = filedialog.askopenfilename(initialdir = "maps/",title = "Select file",filetypes = (("map files","*.map"),("all files","*.*")))
        self.board.map_import(map_file)
        self.reload()

    def export_map(self):
        """ Open the file selector to select to folder to save the map 
        """
        ask_save = filedialog.asksaveasfile(mode='w', initialdir="maps/", defaultextension=".map")
        if ask_save is not None:
            
            name = ask_save.name.split("/")[-1]
            directory = "".join(ask_save.name.split("/")[:-1])
            self.board.map_export(name=ask_save.name)
        
        

    def random_moles(self):
        """ Randomly puts moles on the map
        """
        size_map = self.board.get_size()
        number_of_moles = randint(1,size_map**2)
        self.board.moles = []
        save_quick = self.is_quick
        self.is_quick = True 
        for mole in range(number_of_moles):
            x = randint(0, size_map)
            y = randint(0, size_map)
            self.grass_clicked(x,y)
        self.is_quick = save_quick
        self.board.history.new_map()
        self.reload()

    def new_map(self):
        """ Opens a new map """
        def ok_pressed():
            number = int_text.get()
            if not number.isdigit():
                warning_window = Toplevel()
                warning_window.wm_title("Wrong input")
                l = Label(warning_window, text=f"Please enter a positive number different of 0.\n Entered:{number}")
                l.grid(row=0, column=0)
                ok_button = Button(warning_window, text="OK", command=lambda: warning_window.destroy())
                ok_button.grid(row=1, column=1)
            else:
                self.board = Board(int(number))
            popup_window.destroy()
            self.reload()

        popup_window = Toplevel()
        popup_window.wm_title("New windows file")

        l = Label(popup_window, text="Size of the new map")
        l.grid(row=0, column=0)

        txt = StringVar()
        int_text = Entry(popup_window, textvariable = txt, width=30)
        int_text.grid(row=1, column=0)

        ok_button = Button(popup_window, text="OK", command=lambda: ok_pressed())
        ok_button.grid(row=1, column=1)

    def grass_clicked(self, x, y):
        if self.is_quick:
            self.board.mole_clicked(x,y, True)
            self.reload()

    def mole_clicked(self, x, y):
        """ Callback when a mole is clicked """
        is_finished = self.board.mole_clicked(x, y, self.is_quick)
        self.reload()
        if is_finished:
            self.finish()

    def finish(self):
        popup_window = Toplevel()
        popup_window.wm_title("Congratulations")

        l = Label(popup_window, text=f"Congratulation ! You finished a {self.board.N}x{self.board.N} map !")
        l.grid(row=0, column=0)

    def reload(self):
        """ Reloads the Graphical interface with the map given
        """
        for button in self.master.grid_slaves():
            button.grid_forget()
            button.destroy()
        self._init_grid()

    def undo(self):
        undone = self.board.history.undo()
        if undone is not None:
            self.board.mole_clicked(undone[0], undone[1], False)
            self.reload()

    def next(self):
        forward = self.board.history.next()
        if forward is not None:
            self.board.mole_clicked(forward[0], forward[1], False)
            self.reload()

    def __init__(self, board: Board):
        self.master = Tk()
        self.master.title("DreamAI game")
        self.master.grid()
        self.board = board
        ## Menu
        self.menu = Menu(self.master)
        self.map_menu = Menu(self.menu, tearoff=0)
        self.map_menu.add_command()
        self.map_menu.add_command(label="New", command=self.new_map)
        self.map_menu.add_command(label="Import", command=self.import_map)
        self.map_menu.add_command(label="Export", command=self.export_map)
        self.map_menu.add_separator()
        self.is_quick = False

        self.moles_menu = Menu(self.menu, tearoff=1)
        self.moles_menu.add_checkbutton(label="Manually change state", command=self.change_quick)
        self.moles_menu.add_command(label="Place at random",command=self.random_moles)
        self.menu.add_cascade(label="Map", menu=self.map_menu)
        self.menu.add_cascade(label="Moles", menu=self.moles_menu)
        self.menu.add_command(label="Undo", command=self.undo)
        self.menu.add_command(label="Next", command=self.next)
        self.menu.add_command(label="Help", command=self.show_help)
        self.master.config(menu=self.menu)

        self._init_grid()
        self.master.mainloop()
    
    def _init_grid(self):
        self.buttons = []
        n = self.board.get_size()
        if self.board.N < 4:
            size = 256
        elif self.board.N < 8:
            size = 128
        elif self.board.N < 16:
            size = 64
        else:
            size = 32   
        grass_path = f"images/grass{size}.png"
        mole_path  = f"images/mole{size}.png"
        self.grass_image = PhotoImage(file=r""+grass_path)
        self.mole_image  = PhotoImage(file=r""+mole_path)
        for x in range(n):
            for y in range(n):
                if n * y + x in self.board.moles:
                    image = self.mole_image
                    self.button = Button(self.master, image=image, command= lambda x=x, y=y: self.mole_clicked(x, y), height=size,width=size)
                else:
                    image = self.grass_image
                    self.button = Button(self.master, image=image, command= lambda x=x, y=y: self.grass_clicked(x, y), height=size,width=size)
                
                self.button.grid(row=y, column=x)
        self.buttons.append(self.button)