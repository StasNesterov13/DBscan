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

        self.btn3 = Button(self, text="Загрузить", command=lambda: self.loading(parent), width=22,
                           font="Arial 10",
                           bg='lightblue')
        self.btn3.grid(column=0, row=3, padx=10, pady=10)

        self.btn4 = Button(self, text="Открыть", command=lambda: self.open(parent, self.txt3.get()), width=22,
                           font="Arial 10",
                           bg='lightblue')
        self.btn4.grid(column=2, row=3, padx=10, pady=10)

    def loading(self, parent):
        parent.borehole.Creature(self.txt1.get(), self.txt2.get(), int(self.txt3.get()), parent.var.get())
        parent.lbl1.config(text=f'{parent.borehole.name}')
        self.destroy()

    def open(self, parent, sheet):
        parent.borehole.Read(sheet)
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
        self.filemenu.add_command(label="Сохранить...", command=self.Writer)

        self.methodmenu = Menu(self.mainmenu, tearoff=0)
        self.methodmenu.add_command(label="DBscan", command=self.method_dbscan)
        self.methodmenu.add_command(label="IsolationForest", command=self.method_isolation_forest)

        self.boreholemenu = Menu(self.mainmenu, tearoff=0)
        self.boreholemenu.add_command(label="Отфильтровать...", command=self.Remove)
        self.boreholemenu.add_command(label="Отменить...", command=self.Cancel)
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

        self.method = 0

        self.lbl1 = Label(self, text='Скважина', font="Arial 10", bg='lightblue')
        self.lbl1.pack(fill='x', side='bottom')

        self.lbl2 = Label(self, text='Метод', font="Arial 10", bg='lightblue')
        self.lbl2.pack(fill='x', side='top')

        self.frame1 = Frame(self)
        self.frame1.config(bg='white')
        self.frame1.pack(side='top', fill='x')

        self.frame2 = Frame(self)
        self.frame2.config(bg='lightblue')
        self.frame2.pack(side='right', fill='y', pady=200)

        self.frame3 = Frame(self)
        self.frame3.config(bg='white')
        self.frame3.pack(side='bottom', fill='both')

        self.check_btn1 = Checkbutton(self.frame2, text="График дебита нефти", variable=self.graph_oil, padx=5, pady=5,
                                      bg='lightblue')
        self.check_btn1.grid(column=0, row=0, sticky='w')

        self.check_btn2 = Checkbutton(self.frame2, text="График дебита газа", variable=self.graph_gas, padx=5, pady=5,
                                      bg='lightblue')
        self.check_btn2.grid(column=0, row=1, sticky='w')

        self.check_btn3 = Checkbutton(self.frame2, text="График дебита жидкости", variable=self.graph_water, padx=5,
                                      pady=5,
                                      bg='lightblue')
        self.check_btn3.grid(column=0, row=2, sticky='w')

        self.check_btn4 = Checkbutton(self.frame2, text="График ГФ", variable=self.graph_gf, padx=5, pady=5,
                                      bg='lightblue')
        self.check_btn4.grid(column=0, row=3, sticky='w')

        self.check_btn5 = Checkbutton(self.frame2, text="График давления", variable=self.graph_pressure,
                                      padx=5, pady=5, bg='lightblue')
        self.check_btn5.grid(column=0, row=4, sticky='w')

        self.check_btn6 = Checkbutton(self.frame2, text="График обводненности", variable=self.graph_water_cut,
                                      padx=5, pady=5, bg='lightblue')
        self.check_btn6.grid(column=0, row=5, sticky='w')

        self.btn4 = Button(self.frame2, text="Построить график", command=self.Graphic, font="Arial 10", bg='white',
                           width=15)
        self.btn4.grid(column=0, row=6, padx=5, pady=5)

        self.btn5 = Button(self.frame2, text="Сравнить графики", command=self.Graphics, font="Arial 10", bg='white',
                           width=15)
        self.btn5.grid(column=0, row=7, padx=5, pady=5)

    def download_file(self):
        download = Download(self)
        download.grab_set()

    def method_dbscan(self):
        self.lbl2.config(text=f'DBscan')
        self.method = 1

        self.frame1.destroy()
        self.frame3.destroy()

        self.frame1 = Frame(self)
        self.frame1.config(bg='lightblue')
        self.frame1.pack(side='top', padx=200)

        btn2 = Button(self.frame1, text="K-distances graph", font="Arial 10",
                      command=lambda: self.Epsilon(int(txt2.get())), bg='white', width=15)
        btn2.pack(side='right', padx=5, pady=5)

        btn1 = Button(self.frame1, text="DBscan", command=lambda: self.DBscan(float(txt1.get()), int(txt2.get())),
                      font="Arial 10", bg='white', width=15)
        btn1.pack(side='right', padx=5, pady=5)

        txt2 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt2.pack(side='right', padx=5, pady=5)

        lbl2 = Label(self.frame1, text='MinElements:', font="Arial 10", bg='lightblue')
        lbl2.pack(side='right', padx=5, pady=5)

        txt1 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt1.pack(side='right', padx=5, pady=5)

        lbl1 = Label(self.frame1, text='Eps:', font="Arial 10", bg='lightblue')
        lbl1.pack(side='right', padx=5, pady=5)

    def method_isolation_forest(self):
        self.lbl2.config(text=f'IsolationForest')
        self.method = 1

        self.frame1.destroy()
        self.frame3.destroy()

        self.frame1 = Frame(self)
        self.frame1.config(bg='lightblue')
        self.frame1.pack(side='top')

        btn1 = Button(self.frame1, text="IsolationForest", command=lambda: self.IsolationForest(float(txt1.get())),
                      font="Arial 10", bg='white', width=15)
        btn1.pack(side='right', padx=5, pady=5)

        txt1 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt1.pack(side='right', padx=5, pady=5)

        lbl2 = Label(self.frame1, text='Сontamination:', font="Arial 10", bg='lightblue')
        lbl2.pack(side='right', padx=5, pady=5)

    def DBscan(self, eps, elements):
        self.borehole.df_copy = self.borehole.df.copy()
        dbscan = DBSCAN(eps=eps, min_samples=elements).fit(self.borehole.x_principal)
        self.borehole.df['Cluster'] = dbscan.labels_

    def IsolationForest(self, cont):
        graph = [self.graph_oil.get(), self.graph_gas.get(), self.graph_water.get(), self.graph_gf.get(),
                 self.graph_pressure.get(), self.graph_water_cut.get()]
        forest = IsolationForest(n_estimators=1000, contamination=cont, max_features=sum(graph), random_state=42).fit_predict(
            self.borehole.x_scaled.iloc[:, [i for i, v in enumerate(graph) if v == 1]].values)
        self.borehole.df['Cluster'] = forest

    def Color(self):
        stake_color = len(set(self.borehole.df['Cluster'])) * ['black']
        stake_cluster = set(self.borehole.df['Cluster'])
        clusterColor = dict(zip(stake_cluster, stake_color))
        clusterColor[-1] = 'red'
        return [clusterColor[label] for label in self.borehole.df['Cluster']]

    def Epsilon(self, k):
        self.frame3.destroy()

        self.frame3 = Frame(self)
        self.frame3.config(bg='white')
        self.frame3.pack(side='bottom', fill='both')

        nbrs = NearestNeighbors(n_neighbors=k).fit(self.borehole.x_principal)
        distances, indices = nbrs.kneighbors(self.borehole.x_principal)
        distances = np.sort(distances[:, 1:].mean(axis=1))

        fig = plt.figure(figsize=(15, 10))
        plt.plot(distances)
        plt.title(f'{k}-distance Graph', fontsize=10)
        plt.xlabel('Data Points sorted by distance', fontsize=7)
        plt.ylabel('Epsilon', fontsize=7)
        plt.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        toolbar = NavigationToolbar2Tk(canvas, self.frame3)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack()

    def Graphic(self):
        self.frame3.destroy()

        self.frame3 = Frame(self)
        self.frame3.config(bg='white')
        self.frame3.pack(side='bottom', fill='both')

        fig = plt.figure(figsize=(20, 12))

        graph = [self.graph_oil.get(), self.graph_gas.get(), self.graph_water.get(), self.graph_gf.get(),
                 self.graph_pressure.get(), self.graph_water_cut.get()]
        parametr = [self.borehole.param[6], self.borehole.param[3], self.borehole.param[2], self.borehole.param[10],
                    self.borehole.param[self.borehole.pressure], self.borehole.param[4]]
        if 1 in graph:
            ax = fig.add_subplot()
            ax.scatter(self.borehole.df.index.tolist(), self.borehole.df[parametr[graph.index(1)]], s=8,
                       c=self.Color())
            ax.set(ylabel=f'{parametr[graph.index(1)]}')
            ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        toolbar = NavigationToolbar2Tk(canvas, self.frame3)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack()

    def Graphics(self):
        self.frame3.destroy()

        self.frame3 = Frame(self)
        self.frame3.config(bg='white')
        self.frame3.pack(side='bottom', fill='both')

        fig = plt.figure(figsize=(20, 10))

        graph = [self.graph_oil.get(), self.graph_gas.get(), self.graph_water.get(), self.graph_gf.get(),
                 self.graph_pressure.get(), self.graph_water_cut.get()]
        parametr = [self.borehole.param[6], self.borehole.param[3], self.borehole.param[2], self.borehole.param[10],
                    self.borehole.param[self.borehole.pressure], self.borehole.param[4]]
        if 1 in graph:
            ax1 = fig.add_subplot(2, 1, 1)
            ax1.scatter(self.borehole.df.index.tolist(), self.borehole.df[parametr[graph.index(1)]], s=8,
                        c=self.Color())
            ax1.set(ylabel=f'{parametr[graph.index(1)]}')
            ax1.grid(True)
            graph[graph.index(1)] = 0
            if 1 in graph:
                ax2 = fig.add_subplot(2, 1, 2)
                ax2.scatter(self.borehole.df.index.tolist(), self.borehole.df[parametr[graph.index(1)]], s=8,
                            c=self.Color())
                ax2.set(ylabel=f'{parametr[graph.index(1)]}')
                ax2.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        toolbar = NavigationToolbar2Tk(canvas, self.frame3)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack()

    def Remove(self):
        self.borehole.df_copy = self.borehole.df.copy()
        self.borehole.df = self.borehole.df.loc[self.borehole.df['Cluster'] != -1]
        self.borehole.Standard()

    def Writer(self):
        with pd.ExcelWriter("Two.xlsx", mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            self.borehole.df.iloc[:, :-1].to_excel(writer, sheet_name=f'{self.borehole.name}')

    def Cancel(self):
        self.borehole.df = self.borehole.df_copy.copy()


if __name__ == '__main__':
    widget = Widget()
    widget.mainloop()
