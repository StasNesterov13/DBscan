from tkinter import *
from Borehole import *


def clicked():
    global borehole
    borehole = Borehole(txt1.get(), txt2.get(), int(txt3.get()))
    borehole.Creature()
    lbl = Label(window, text=borehole.name, width=15, height=1)
    lbl.grid(column=0, row=1)


def read():
    global borehole
    borehole = Borehole()
    borehole.Read()
    lbl = Label(window, text=borehole.name, width=15, height=1)
    lbl.grid(column=0, row=1)


def epsilon():
    borehole.Epsilon()
    plt.show()


def scan():
    borehole.Scan(float(txt4.get()), int(txt5.get()))


def clustering():
    borehole.Clustering()


def graphics_oil():
    borehole.Graphics_oil()


def graphics_gas():
    borehole.Graphics_gas()


def graphics_gf():
    borehole.Graphics_gf()


def graphics_water():
    borehole.Graphics_water()


def graphics_pressure():
    borehole.Graphics_pressure()


def remove():
    borehole.Remove()


if __name__ == '__main__':
    window = Tk()
    window.title("Debit")
    window.geometry('650x450')

    txt1 = Entry(window, width=20)
    txt1.grid(column=1, row=0)
    txt2 = Entry(window, width=20)
    txt2.grid(column=1, row=1)
    txt3 = Entry(window, width=20)
    txt3.grid(column=1, row=2)
    btn1 = Button(window, text="Загрузить данные скважины", command=clicked, height=3, width=30)
    btn1.grid(column=1, row=3)
    btn2 = Button(window, text="График расстояний", command=epsilon, height=3, width=30)
    btn2.grid(column=1, row=6)
    btn3 = Button(window, text="Удалить лишние точки", command=remove, height=3, width=30)
    btn3.grid(column=1, row=5)
    btn11 = Button(window, text="Прочитать данные скважины", command=read, height=3, width=30)
    btn11.grid(column=1, row=4)

    txt4 = Entry(window, width=20)
    txt4.grid(column=2, row=0)
    txt5 = Entry(window, width=20)
    txt5.grid(column=2, row=1)
    btn4 = Button(window, text="DBscan", command=scan, height=3, width=30)
    btn4.grid(column=2, row=3)
    btn5 = Button(window, text="Кластеризация", command=clustering, height=3, width=30)
    btn5.grid(column=2, row=4)

    btn6 = Button(window, text="График дебита нефти", command=graphics_oil, height=3, width=30)
    btn6.grid(column=0, row=3)
    btn7 = Button(window, text="График дебита газа", command=graphics_gas, height=3, width=30)
    btn7.grid(column=0, row=4)
    btn8 = Button(window, text="График ГФ", command=graphics_gf, height=3, width=30)
    btn8.grid(column=0, row=5)
    btn9 = Button(window, text="График обводненности", command=graphics_water, height=3, width=30)
    btn9.grid(column=0, row=6)
    btn10 = Button(window, text="График давления", command=graphics_pressure, height=3, width=30)
    btn10.grid(column=0, row=7)

    window.mainloop()
