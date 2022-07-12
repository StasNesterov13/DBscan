from tkinter import *
from Borehole import *


def clicked():
    global borehole
    borehole = Borehole()
    borehole.Creature(txt1.get(), txt2.get(), int(txt3.get()))
    lbl1 = Label(window, text=borehole.name, width=15, height=1)
    lbl1.grid(column=0, row=1)


def read():
    global borehole
    borehole = Borehole()
    borehole.Read()
    lbl1 = Label(window, text=borehole.name, width=15, height=1)
    lbl1.grid(column=0, row=1)


def epsilon():
    borehole.Epsilon(int(txt5.get()))
    plt.show()


def dbscan():
    borehole.DBscan(float(txt4.get()), int(txt5.get()))


def means():
    borehole.Means()


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


def writer():
    borehole.Writer()


if __name__ == '__main__':
    window = Tk()
    window.title("Debit")
    window.geometry('650x450')

    lbl2 = Label(window, text='Первый столбец', width=15, height=1)
    lbl2.grid(column=1, row=0)
    txt1 = Entry(window, width=20)
    txt1.grid(column=1, row=1)
    lbl3 = Label(window, text='Последний столбец', width=15, height=1)
    lbl3.grid(column=1, row=2)
    txt2 = Entry(window, width=20)
    txt2.grid(column=1, row=3)
    lbl4 = Label(window, text='Номер строки', width=15, height=1)
    lbl4.grid(column=1, row=4)
    txt3 = Entry(window, width=20)
    txt3.grid(column=1, row=5)
    btn1 = Button(window, text="Загрузить данные скважины", command=clicked, height=2, width=30)
    btn1.grid(column=1, row=6)
    btn2 = Button(window, text="Использовать данные скважины", command=read, height=2, width=30)
    btn2.grid(column=1, row=7)
    btn3 = Button(window, text="Удалить лишние точки", command=remove, height=2, width=30)
    btn3.grid(column=1, row=8)
    btn4 = Button(window, text="Сохранить данные скважины", command=writer, height=2, width=30)
    btn4.grid(column=1, row=9)

    lbl5 = Label(window, text='Eps', width=15, height=1)
    lbl5.grid(column=2, row=0)
    txt4 = Entry(window, width=20)
    txt4.grid(column=2, row=1)
    lbl6 = Label(window, text='MinElements', width=15, height=1)
    lbl6.grid(column=2, row=2)
    txt5 = Entry(window, width=20)
    txt5.grid(column=2, row=3)
    btn5 = Button(window, text="K-distance Graph", command=epsilon, height=2, width=30)
    btn5.grid(column=2, row=6)
    btn6 = Button(window, text="DBscan", command=dbscan, height=2, width=30)
    btn6.grid(column=2, row=7)
    btn7 = Button(window, text="Кластеризация", command=clustering, height=2, width=30)
    btn7.grid(column=2, row=8)
    btn13 = Button(window, text="K-means", command=means, height=2, width=30)
    btn13.grid(column=2, row=9)

    btn8 = Button(window, text="График дебита нефти", command=graphics_oil, height=2, width=30)
    btn8.grid(column=0, row=6)
    btn9 = Button(window, text="График дебита газа", command=graphics_gas, height=2, width=30)
    btn9.grid(column=0, row=7)
    btn10 = Button(window, text="График ГФ", command=graphics_gf, height=2, width=30)
    btn10.grid(column=0, row=8)
    btn11 = Button(window, text="График обводненности", command=graphics_water, height=2, width=30)
    btn11.grid(column=0, row=9)
    btn12 = Button(window, text="График давления", command=graphics_pressure, height=2, width=30)
    btn12.grid(column=0, row=10)

    window.mainloop()
