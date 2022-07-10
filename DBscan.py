from tkinter import *
from Borehole import *


def clicked():
    global borehole
    borehole = Borehole(txt1.get(), txt2.get(), txt3.get())
    borehole.Creature()
    borehole.Read()
    lbl = Label(window, text=borehole.number_data, width=3, height=1)
    lbl.grid(column=1, row=7)


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


def read():
    global borehole
    borehole = Borehole()
    borehole.Read()
    lbl = Label(window, text=borehole.number_data, width=3, height=1)
    lbl.grid(column=1, row=7)


if __name__ == '__main__':
    window = Tk()
    window.title("Debit")
    window.geometry('425x250')

    txt1 = Entry(window, width=10)
    txt1.grid(column=1, row=0)
    txt2 = Entry(window, width=10)
    txt2.grid(column=1, row=1)
    txt3 = Entry(window, width=10)
    txt3.grid(column=1, row=2)
    btn1 = Button(window, text="Загрузить данные скважины", command=clicked)
    btn1.grid(column=1, row=3)
    btn2 = Button(window, text="График расстояний", command=epsilon)
    btn2.grid(column=1, row=4)
    btn3 = Button(window, text="Удалить лишние точки", command=remove)
    btn3.grid(column=1, row=5)
    btn11 = Button(window, text="Прочитать данные скважины", command=read)
    btn11.grid(column=1, row=6)

    txt4 = Entry(window, width=10)
    txt4.grid(column=2, row=0)
    txt5 = Entry(window, width=10)
    txt5.grid(column=2, row=1)
    btn4 = Button(window, text="Сканирование", command=scan)
    btn4.grid(column=2, row=2)
    btn5 = Button(window, text="Кластеризация", command=clustering)
    btn5.grid(column=2, row=3)

    btn6 = Button(window, text="График дебита нефти", command=graphics_oil)
    btn6.grid(column=0, row=0)
    btn7 = Button(window, text="График дебита газа", command=graphics_gas)
    btn7.grid(column=0, row=1)
    btn8 = Button(window, text="График ГФ", command=graphics_gf)
    btn8.grid(column=0, row=2)
    btn9 = Button(window, text="График обводненности", command=graphics_water)
    btn9.grid(column=0, row=3)
    btn10 = Button(window, text="График давления", command=graphics_pressure)
    btn10.grid(column=0, row=4)

    window.mainloop()
