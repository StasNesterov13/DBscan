from tkinter import *
from Borehole import *


class Widget(Tk):
    def __init__(self):
        super().__init__()
        self.title("Data filtering")
        self.geometry('750x450')


if __name__ == '__main__':
    widget = Widget()
    widget.mainloop()
