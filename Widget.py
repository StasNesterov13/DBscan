from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from tkinter.ttk import Notebook, Frame
from Borehole import *


class Widget(Tk):
    def __init__(self):
        super().__init__()
        self.title('Data filtering')
        self.geometry('1000x600')
        self.mainmenu = Menu(self)
        self.config(menu=self.mainmenu)

        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label="New...")
        self.filemenu.add_command(label="Open..")
        self.filemenu.add_command(label="Save...")

        self.methodmenu = Menu(self.mainmenu, tearoff=0)
        self.methodmenu.add_command(label="DBscan", command=self.dbscan)

        self.mainmenu.add_cascade(label="File",
                                  menu=self.filemenu)
        self.mainmenu.add_cascade(label="Method",
                                  menu=self.methodmenu)
        self.borehole = Borehole()

    def new(self):
        pass

    def open(self):
        self.borehole.Read()

    def dbscan(self):
        pass


if __name__ == '__main__':
    widget = Widget()
    widget.mainloop()
