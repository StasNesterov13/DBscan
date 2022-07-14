from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from Borehole import *


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Data filtering")
        self.geometry('750x450')
        for i in range(3):
            Grid.columnconfigure(self, i, weight=1)

        for i in range(12):
            Grid.rowconfigure(self, i, weight=1)

        self.txt = Entry(self, width=20, font="Arial 12", justify='center')
        self.txt.grid(column=0, row=3, sticky="NSEW")
        self.lbl7 = Label(self, text='Название скважины', width=15, height=1, font="Arial 12")
        self.lbl7.grid(column=0, row=2, sticky="NSEW")
        self.bar = Progressbar(self, orient="horizontal", mode="determinate", maximum=100, value=0, length=200)
        self.bar.grid(column=0, row=4, sticky="NSEW")
        self.btn8 = Button(self, text="График дебита нефти", command=self.graphics_oil, height=2, width=30,
                           font="Arial 12")
        self.btn8.grid(column=0, row=6, sticky="NSEW")
        self.btn9 = Button(self, text="График дебита газа", command=self.graphics_gas, height=2, width=30,
                           font="Arial 12")
        self.btn9.grid(column=0, row=7, sticky="NSEW")
        self.btn10 = Button(self, text="График ГФ", command=self.graphics_gf, height=2, width=30, font="Arial 12")
        self.btn10.grid(column=0, row=8, sticky="NSEW")
        self.btn11 = Button(self, text="График дебита воды", command=self.graphics_water, height=2, width=30,
                            font="Arial 12")
        self.btn11.grid(column=0, row=9, sticky="NSEW")
        self.btn12 = Button(self, text="График давления", command=self.graphics_pressure, height=2, width=30,
                            font="Arial 12")
        self.btn12.grid(column=0, row=10, sticky="NSEW")
        self.btn15 = Button(self, text="График обводненности", command=self.graphics_water_cut, height=2, width=30,
                            font="Arial 12")
        self.btn15.grid(column=0, row=11, sticky="NSEW")

        self.lbl2 = Label(self, text='Первый столбец', width=15, height=1, font="Arial 12")
        self.lbl2.grid(column=1, row=0, sticky="NSEW")
        self.txt1 = Entry(self, width=20, font="Arial 12", justify='center')
        self.txt1.grid(column=1, row=1, sticky="NSEW")
        self.lbl3 = Label(self, text='Последний столбец', width=15, height=1, font="Arial 12")
        self.lbl3.grid(column=1, row=2, sticky="NSEW")
        self.txt2 = Entry(self, width=2, font="Arial 12", justify='center')
        self.txt2.grid(column=1, row=3, sticky="NSEW")
        self.lbl4 = Label(self, text='Номер строки', width=15, height=1, font="Arial 12")
        self.lbl4.grid(column=1, row=4, sticky="NSEW")
        self.txt3 = Entry(self, width=20, font="Arial 12", justify='center')
        self.txt3.grid(column=1, row=5, sticky="NSEW")
        self.btn1 = Button(self, text="Загрузить данные скважины", command=self.clicked, height=2, width=30,
                           font="Arial 12")
        self.btn1.grid(column=1, row=8, sticky="NSEW")
        self.btn2 = Button(self, text="Использовать данные скважины", command=self.read, height=2, width=30,
                           font="Arial 12")
        self.btn2.grid(column=1, row=9, sticky="NSEW")
        self.btn3 = Button(self, text="Удалить лишние точки", command=self.remove, height=2, width=30, font="Arial 12")
        self.btn3.grid(column=1, row=10, sticky="NSEW")
        self.btn4 = Button(self, text="Сохранить данные скважины", command=self.writer, height=2, width=30,
                           font="Arial 12")
        self.btn4.grid(column=1, row=11, sticky="NSEW")
        self.var = IntVar()
        self.btn13 = Radiobutton(text="Рприем, атм", variable=self.var, value=14, font="Arial 12")
        self.btn13.grid(column=1, row=6, sticky="NSEW")
        self.btn14 = Radiobutton(text="Рзаб замер", variable=self.var, value=16, font="Arial 12")
        self.btn14.grid(column=1, row=7, sticky="NSEW")

        self.lbl5 = Label(self, text='Eps', width=15, height=1, font="Arial 12")
        self.lbl5.grid(column=2, row=0, sticky="NSEW")
        self.txt4 = Entry(self, width=20, font="Arial 12", justify='center')
        self.txt4.grid(column=2, row=1, sticky="NSEW")
        self.lbl6 = Label(self, text='MinElements', width=15, height=1, font="Arial 12")
        self.lbl6.grid(column=2, row=2, sticky="NSEW")
        self.txt5 = Entry(self, width=20, font="Arial 12", justify='center')
        self.txt5.grid(column=2, row=3, sticky="NSEW")
        self.btn5 = Button(self, text="K-distance Graph", command=self.epsilon, height=2, width=30, font="Arial 12")
        self.btn5.grid(column=2, row=6, sticky="NSEW")
        self.btn6 = Button(self, text="DBscan", command=self.dbscan, height=2, width=30, font="Arial 12")
        self.btn6.grid(column=2, row=7, sticky="NSEW")
        self.btn7 = Button(self, text="Кластеризация", command=self.clustering, height=2, width=30, font="Arial 12")
        self.btn7.grid(column=2, row=8, sticky="NSEW")

    def clicked(self):
        try:
            global borehole
            borehole = Borehole()
            for progress in borehole.Creature(self.txt1.get(), self.txt2.get(), int(self.txt3.get()), self.var.get()):
                self.bar['value'] = progress
                self.update()
            self.txt.insert(0, borehole.name)

        except ValueError:
            return messagebox.showinfo('Error',
                                       'Необходимо ввести все значения для загрузки данных скважины и выбрать тип давления')

    def read(self):
        try:
            global borehole
            borehole = Borehole()
            borehole.Read()
            self.txt.insert(0, borehole.name)
        except FileNotFoundError:
            return messagebox.showinfo('Error',
                                       'Необходимо сначала загрузить данные сквважины')

    def epsilon(self):
        try:
            borehole.Epsilon(int(self.txt5.get()))
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')
        except ValueError:
            return messagebox.showinfo('Error',
                                       'Необходимо выбрать количество элементов для K-distances Graph')

    def dbscan(self):
        try:
            borehole.DBscan(float(self.txt4.get()), int(self.txt5.get()))
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')
        except ValueError:
            return messagebox.showinfo('Error',
                                       'Необходимо выбрать диапазон и количество элементов для метода DBscan')

    @staticmethod
    def clustering():
        try:
            borehole.Clustering()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')

    @staticmethod
    def graphics_oil():
        try:
            borehole.Graphics_oil()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')

    @staticmethod
    def graphics_gas():
        try:
            borehole.Graphics_gas()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')

    @staticmethod
    def graphics_gf():
        try:
            borehole.Graphics_gf()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')

    @staticmethod
    def graphics_water():
        try:
            borehole.Graphics_water()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')

    @staticmethod
    def graphics_pressure():
        try:
            borehole.Graphics_pressure()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')

    @staticmethod
    def graphics_water_cut():
        try:
            borehole.Graphics_water_cut()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')

    @staticmethod
    def remove():
        try:
            borehole.Remove()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')

    @staticmethod
    def writer():
        try:
            borehole.Writer()
        except NameError:
            return messagebox.showinfo('Error',
                                       'Необходимо загрузить данные скважины или использовать уже загруженные данные скважины')


if __name__ == '__main__':
    window = App()
    window.mainloop()
