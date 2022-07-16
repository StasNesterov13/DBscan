from tkinter import *
from Borehole import *
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk, FigureCanvasTkAgg


class Download(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Загрузка данных скважины')
        self.geometry('575x200')
        self.configure(bg='white')
        self.resizable(width=0, height=0)

        self.txt1 = Entry(self, width=20, font="Arial 10", justify='center', bg='lightblue')
        self.txt1.grid(column=1, row=0, padx=5, pady=5)

        self.lbl1 = Label(self, text='Дата начала', width=20, font="Arial 10", bg='white')
        self.lbl1.grid(column=0, row=0, padx=5, pady=5)

        self.txt2 = Entry(self, width=20, font="Arial 10", justify='center', bg='lightblue')
        self.txt2.grid(column=1, row=1, padx=5, pady=5)

        self.lbl2 = Label(self, text='Дата окончания', width=20, font="Arial 10", bg='white')
        self.lbl2.grid(column=0, row=1, padx=5, pady=5)

        self.txt3 = Entry(self, width=20, font="Arial 10", justify='center', bg='lightblue')
        self.txt3.grid(column=1, row=2, padx=5, pady=5)

        self.lbl3 = Label(self, text='Название скважины', width=20, font="Arial 10", bg='white')
        self.lbl3.grid(column=0, row=2, padx=5, pady=5)

        self.lbl4 = Label(self, text='Тип давления', width=21, font="Arial 10", bg='white')
        self.lbl4.grid(column=2, row=0, padx=5, pady=5)

        self.btn1 = Radiobutton(self, text="Рприем, атм", variable=parent.var, value=14, width=18, font="Arial 10",
                                bg='white')
        self.btn1.grid(column=2, row=1, padx=5, pady=5)

        self.btn2 = Radiobutton(self, text="Рзаб замер", variable=parent.var, value=16, width=18, font="Arial 10",
                                bg='white')
        self.btn2.grid(column=2, row=2, padx=5, pady=5)

        self.btn3 = Button(self, text="Загрузить данные скважины", command=lambda: self.loading(parent), width=22,
                           font="Arial 10",
                           bg='lightblue')
        self.btn3.grid(column=0, row=3, padx=10, pady=10)

        self.btn4 = Button(self, text="Открыть данные скважины", command=lambda: self.open(parent), width=22,
                           font="Arial 10",
                           bg='lightblue')
        self.btn4.grid(column=2, row=3, padx=10, pady=10)

    def loading(self, parent):
        parent.borehole.Creature(self.txt1.get(), self.txt2.get(), int(self.txt3.get()), parent.var.get())
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
        self.geometry('1440x720')
        self.configure(bg='white')
        self.resizable(width=0, height=0)
        self.mainmenu = Menu(self)
        self.config(menu=self.mainmenu)

        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label="Загрузить или открыть...", command=self.download_file)
        self.filemenu.add_command(label="Сохранить...")

        self.methodmenu = Menu(self.mainmenu, tearoff=0)
        self.methodmenu.add_command(label="DBscan", command=self.method_dbscan)

        self.boreholemenu = Menu(self.mainmenu, tearoff=0)
        self.boreholemenu.add_command(label="Отфильтровать...")
        self.boreholemenu.add_command(label="Отменить...")

        self.mainmenu.add_cascade(label="Файл",
                                  menu=self.filemenu)
        self.mainmenu.add_cascade(label="Метод",
                                  menu=self.methodmenu)
        self.mainmenu.add_cascade(label="Скважина",
                                  menu=self.boreholemenu)

        self.borehole = Borehole()

        self.var = IntVar()
        self.graph_oil = IntVar(value=0)
        self.graph_gas = IntVar()
        self.graph_water = IntVar()
        self.graph_gf = IntVar()
        self.graph_pressure = IntVar()
        self.graph_water_cut = IntVar()

        self.lbl1 = Label(self, text='Скважина', font="Arial 10", bg='lightblue')
        self.lbl1.pack(fill='both', side='bottom')

        self.lbl2 = Label(self, text='Метод', font="Arial 10", bg='lightblue')
        self.lbl2.pack(fill='both', side='top')

        self.frame1 = Frame(self)
        self.frame1.config(bg='white')
        self.frame1.pack(side='top')

        self.frame2 = Frame(self)
        self.frame2.config(bg='white')
        self.frame2.pack(side='top')

        self.frame3 = Frame(self)
        self.frame3.config(bg='white')
        self.frame3.pack(side='right')

        self.frame4 = Frame(self)
        self.frame3.config(bg='white')
        self.frame4.pack(side='bottom')

    def download_file(self):
        download = Download(self)
        download.grab_set()

    def method_dbscan(self):
        self.lbl2.config(text=f'DBscan')

        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()

        self.frame1 = Frame(self)
        self.frame1.config(bg='white')
        self.frame1.pack(side='top', fill='x', padx=550)

        self.frame2 = Frame(self)
        self.frame2.config(bg='white')
        self.frame2.pack(side='top', fill='x', padx=575)

        self.frame3 = Frame(self)
        self.frame3.config(bg='white')
        self.frame3.pack(side='right', fill='y')

        lbl1 = Label(self.frame1, text='Eps:', font="Arial 10", bg='white')
        lbl1.pack(side='left', padx=10, pady=10)

        txt1 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='lightblue')
        txt1.pack(side='left', padx=10, pady=10)

        lbl2 = Label(self.frame1, text='MinElements:', font="Arial 10", bg='white')
        lbl2.pack(side='left', padx=10, pady=10)

        txt2 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='lightblue')
        txt2.pack(side='left', padx=10, pady=10)

        btn1 = Button(self.frame2, text="Clustering", font="Arial 10", bg='lightblue', width=15)
        btn1.grid(column=0, row=0, padx=5, pady=5)

        btn2 = Button(self.frame2, text="DBscan", font="Arial 10", bg='lightblue', width=15)
        btn2.grid(column=1, row=0, padx=5, pady=5)

        btn3 = Button(self.frame2, text="K-distances graph", font="Arial 10",
                      command=lambda: self.Epsilon(int(txt2.get())), bg='lightblue', width=15)
        btn3.grid(columnspan=2, row=1, padx=5, pady=5)

        check_btn1 = Checkbutton(self.frame3, text="График дебита нефти", variable=self.graph_oil, padx=15,
                                 pady=10, bg='white')
        check_btn1.grid(column=0, row=0, sticky='w')

        check_btn2 = Checkbutton(self.frame3, text="График дебита газа", variable=self.graph_gas, padx=15,
                                 pady=10, bg='white')
        check_btn2.grid(column=0, row=1, sticky='w')

        check_btn3 = Checkbutton(self.frame3, text="График дебита жидкости", variable=self.graph_water, padx=15,
                                 pady=10, bg='white')
        check_btn3.grid(column=0, row=2, sticky='w')

        check_btn4 = Checkbutton(self.frame3, text="График ГФ", variable=self.graph_gf, padx=15,
                                 pady=10, bg='white')
        check_btn4.grid(column=0, row=3, sticky='w')

        check_btn5 = Checkbutton(self.frame3, text="График давления", variable=self.graph_pressure,
                                 padx=15, pady=10, bg='white')
        check_btn5.grid(column=0, row=4, sticky='w')

        check_btn6 = Checkbutton(self.frame3, text="График обводненности", variable=self.graph_water_cut,
                                 padx=15, pady=10, bg='white')
        check_btn6.grid(column=0, row=5, sticky='w')

        btn4 = Button(self.frame3, text="Построить график", command=self.Graphics, font="Arial 10", bg='lightblue',
                      width=15)
        btn4.grid(column=0, row=6, padx=5, pady=5)

    def Color(self, rainbow):
        if rainbow:
            stake_color = list(palette.CSS4_COLORS.values())[10:]
        else:
            stake_color = len(set(self.borehole.df['Cluster'])) * ['black']
        stake_cluster = set(self.borehole.df['Cluster'])
        clusterColor = dict(zip(stake_cluster, stake_color))
        clusterColor[-1] = 'red'
        return [clusterColor[label] for label in self.borehole.df['Cluster']]

    def Epsilon(self, k):
        self.frame4.destroy()

        self.frame4 = Frame(self)
        self.frame4.config(bg='white')
        self.frame4.pack(side='bottom', fill='both')

        nbrs = NearestNeighbors(n_neighbors=k).fit(self.borehole.x_principal)
        distances, indices = nbrs.kneighbors(self.borehole.x_principal)
        distances = np.sort(distances[:, 1:].mean(axis=1))

        fig = plt.figure(figsize=(15, 10))
        plt.plot(distances)
        plt.title(f'{k}-distance Graph', fontsize=10)
        plt.xlabel('Data Points sorted by distance', fontsize=7)
        plt.ylabel('Epsilon', fontsize=7)
        plt.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame4)
        toolbar = NavigationToolbar2Tk(canvas, self.frame4)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack()

    def Graphics(self):
        self.frame4.destroy()

        self.frame4 = Frame(self)
        self.frame4.config(bg='white')
        self.frame4.pack(side='bottom', fill='both')
        fig = plt.figure(figsize=(20, 10))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        if self.graph_oil.get():
            ax1.scatter(self.borehole.df.index.tolist(), self.borehole.df[self.borehole.param[6]], s=15, c='red')
        if self.graph_gas.get():
            ax2.scatter(self.borehole.df.index.tolist(), self.borehole.df[self.borehole.param[3]], s=15, c='blue')

        canvas = FigureCanvasTkAgg(fig, master=self.frame4)
        toolbar = NavigationToolbar2Tk(canvas, self.frame4)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == '__main__':
    widget = Widget()
    widget.mainloop()
