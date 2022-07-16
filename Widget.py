from tkinter import *
from Borehole import *


class Download(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Загрузка данных скважины')
        self.geometry('625x200')
        self.configure(bg='lightblue')
        self.resizable(width=0, height=0)

        self.txt1_dd = Entry(self, width=20, font="Arial 10", justify='center')
        self.txt1_dd.grid(column=1, row=0, padx=5, pady=5)

        self.lbl1_dd = Label(self, text='Дата начала', width=20, font="Arial 10", bg='lightblue', justify='left')
        self.lbl1_dd.grid(column=0, row=0, padx=5, pady=5)

        self.txt2_dd = Entry(self, width=20, font="Arial 10", justify='center')
        self.txt2_dd.grid(column=1, row=1,  padx=5, pady=5)

        self.lbl2_dd = Label(self, text='Дата окончания', width=20, font="Arial 10", bg='lightblue', justify='left')
        self.lbl2_dd.grid(column=0, row=1,  padx=5, pady=5)

        self.txt3_dd = Entry(self, width=20, font="Arial 10", justify='center')
        self.txt3_dd.grid(column=1, row=2, padx=5, pady=5)

        self.lbl3_dd = Label(self, text='Название скважины', width=20, font="Arial 10", bg='lightblue', justify='left')
        self.lbl3_dd.grid(column=0, row=2, padx=5, pady=5)

        self.btn1_dd = Radiobutton(self, text="Рприем, атм", variable=parent.var, value=14, width=20, font="Arial 10",
                                   bg='lightblue')
        self.btn1_dd.grid(column=2, row=0, padx=5, pady=5)

        self.btn2_dd = Radiobutton(self, text="Рзаб замер", variable=parent.var, value=16, width=20, font="Arial 10",
                                   bg='lightblue')
        self.btn2_dd.grid(column=2, row=2, padx=5, pady=5)

        self.btn3_dd = Button(self, text="Загрузить данные скважины", command=lambda: self.loading(parent), width=25,
                              font="Arial 10",
                              bg='white')
        self.btn3_dd.grid(column=0, row=3, padx=10, pady=10)

        self.btn4_dd = Button(self, text="Открыть данные скважины", command=lambda: self.open(parent), width=25,
                              font="Arial 10",
                              bg='white')
        self.btn4_dd.grid(column=2, row=3, padx=10, pady=10)

    def loading(self, parent):
        parent.borehole.Creature(self.txt1_dd.get(), self.txt2_dd.get(), int(self.txt3_dd.get()), parent.var.get())
        parent.lbl1.config(text=f'{parent.borehole.name}')
        self.destroy()

    def open(self, parent):
        parent.borehole.Read()
        parent.lbl1.config(text=f'{parent.borehole.name}')
        self.destroy()


class Widget(Tk):
    def __init__(self):
        super().__init__()
        self.title('Фильтрация данных')
        self.geometry('1000x600')
        self.configure(bg='white')
        self.mainmenu = Menu(self)
        self.config(menu=self.mainmenu)

        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label="Загрузить или открыть...", command=self.download_file)
        self.filemenu.add_command(label="Сохранить...")

        self.methodmenu = Menu(self.mainmenu, tearoff=0)
        self.methodmenu.add_command(label="DBscan", command=self.method_dbscan)

        self.mainmenu.add_cascade(label="Файл",
                                  menu=self.filemenu)
        self.mainmenu.add_cascade(label="Метод",
                                  menu=self.methodmenu)
        self.borehole = Borehole()
        self.var = IntVar()

        self.method = 'DBscan'

        self.lbl1 = Label(self, text=self.borehole.name, font="Arial 10", bg='lightblue')
        self.lbl1.pack(fill='both', side='bottom')

        self.lbl2 = Label(self, text=self.method, font="Arial 10", bg='lightblue')
        self.lbl2.pack(fill='both', side='top')

    def download_file(self):
        download = Download(self)
        download.grab_set()

    def method_dbscan(self):
        pass

    def clicked(self):
        pass

    def loading(self):
        self.borehole.Creature(self.txt1_dd.get(), self.txt2_dd.get(), int(self.txt3_dd.get()), self.var.get())


if __name__ == '__main__':
    widget = Widget()
    widget.mainloop()
