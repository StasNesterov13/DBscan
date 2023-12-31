from tkinter import *
from tkinter import messagebox

from Borehole import *
from numpy import std
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk, FigureCanvasTkAgg
from scipy.interpolate import splrep, splev
from scipy import stats


class Download(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Загрузка данных скважины')
        self.geometry('400x200')
        self.configure(bg='white')
        self.resizable(width=0, height=0)
        self.boreholes = openpyxl.load_workbook('One.xlsx').sheetnames
        self.boreholevar = StringVar(self)
        self.boreholevar.set(self.boreholes[0])

        self.txt1 = Entry(self, width=20, font="Arial 10", justify='center', bg='lightblue')
        self.txt1.grid(column=0, row=0, padx=5, pady=5)

        self.txt2 = Entry(self, width=20, font="Arial 10", justify='center', bg='lightblue')
        self.txt2.grid(column=0, row=1, padx=5, pady=5)

        self.txt3 = OptionMenu(self, self.boreholevar, *self.boreholes)
        self.txt3.config(width=20, bg='white')
        self.txt3.grid(column=0, row=2, padx=5, pady=5)

        self.txt4 = Entry(self, width=20, font="Arial 10", justify='center', bg='lightblue')
        self.txt4.grid(column=1, row=0, padx=5, pady=5)

        self.btn1 = Radiobutton(self, text="Рприем, атм", variable=parent.var, value=14, width=20, font="Arial 10",
                                bg='white')
        self.btn1.grid(column=1, row=1, padx=5, pady=5)

        self.btn2 = Radiobutton(self, text="Рзаб замер", variable=parent.var, value=16, width=20, font="Arial 10",
                                bg='white')
        self.btn2.grid(column=1, row=2, padx=5, pady=5)

        self.btn3 = Button(self, text="Загрузить", command=lambda: self.Loading(parent), width=20,
                           font="Arial 10",
                           bg='lightblue')
        self.btn3.grid(column=1, row=3, padx=10, pady=10)

        self.btn4 = Button(self, text="Открыть", command=lambda: self.Open(parent, self.boreholevar.get()), width=20,
                           font="Arial 10",
                           bg='lightblue')
        self.btn4.grid(column=0, row=3, padx=10, pady=10)

    def Loading(self, parent):
        parent.borehole.Creature('E', 'BNQ', int(self.txt4.get()), parent.var.get())

    def Open(self, parent, sheet):
        parent.borehole.Read(sheet)
        parent.borehole_copy.Read(sheet)
        parent.borehole_list.clear()
        parent.borehole_list.append(parent.borehole.df.copy(deep=True))

        parent.lbl1.config(text=f'{parent.borehole.name} {parent.borehole.df.columns[-2]}')

        parent.Entry_date()

        parent.Graphic()
        parent.deiconify()
        self.destroy()


class Widget(Tk):
    def __init__(self):
        super().__init__()
        self.title('Фильтрация данных')
        self.geometry('1440x720')
        self.configure(bg='white')

        self.mainmenu = Menu(self)
        self.config(menu=self.mainmenu)

        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label="Загрузить или открыть...", command=self.Download_file)
        self.filemenu.add_command(label="Сохранить...", command=self.Writer)

        self.methodmenu = Menu(self.mainmenu, tearoff=0)
        self.methodmenu.add_command(label="DBscan", command=self.Method_dbscan)
        self.methodmenu.add_command(label="IsolationForest", command=self.Method_isolation_forest)
        self.methodmenu.add_command(label="LocalOutlierFactor", command=self.Method_local_outlier_factor)
        self.methodmenu.add_command(label="Z-Score", command=self.Method_Z_score)
        self.methodmenu.add_command(label="IQR", command=self.IQR)
        self.methodmenu.add_command(label="MA", command=self.Method_MA)

        self.datamenu = Menu(self.mainmenu, tearoff=0)
        self.datamenu.add_radiobutton(label="All...",
                                      command=lambda: [self.data_part.set(1), self.All()])
        self.datamenu.add_radiobutton(label="Part...",
                                      command=lambda: [self.data_part.set(0), self.Part()])

        self.boreholemenu = Menu(self.mainmenu, tearoff=0)

        self.graphicmenu = Menu(self.boreholemenu, tearoff=0)
        self.graphicmenu.add_radiobutton(label="Поточечный...",
                                         command=lambda: [self.graphic_mode.set(1), self.Graphic()])

        self.graphicmenu.add_radiobutton(label="Линейный...",
                                         command=lambda: [self.graphic_mode.set(0), self.Graphic()])

        self.graphicmenu.add_radiobutton(label="Линейный с точками...",
                                         command=lambda: [self.graphic_mode.set(2), self.Graphic()])

        self.boreholemenu.add_cascade(label="График...", menu=self.graphicmenu)
        self.boreholemenu.add_command(label="Отфильтровать...", command=self.Remove)
        self.boreholemenu.add_command(label="Отменить...", command=self.Cancel)

        self.mainmenu.add_cascade(label="Файл",
                                  menu=self.filemenu)
        self.mainmenu.add_cascade(label="Метод",
                                  menu=self.methodmenu)
        self.mainmenu.add_cascade(label="Обработка",
                                  menu=self.boreholemenu)
        self.mainmenu.add_cascade(label="Данные",
                                  menu=self.datamenu)

        self.borehole = Borehole()
        self.borehole_copy = Borehole()
        self.borehole_list = []

        self.var = IntVar(value=14)
        self.graph_oil = IntVar(value=1)
        self.graph_gas = IntVar()
        self.graph_water = IntVar()
        self.graph_gf = IntVar()
        self.graph_pressure = IntVar()
        self.graph_water_cut = IntVar()
        self.data_part = IntVar(value=1)
        self.dbscan_mode = IntVar(value=0)
        self.graphic_mode = IntVar(value=1)

        self.lbl1 = Label(self, text='Скважина', font="Arial 10", bg='lightblue')
        self.lbl1.pack(fill='x', side='bottom')

        self.lbl2 = Label(self, text='Метод', font="Arial 10", bg='lightblue')
        self.lbl2.pack(fill='x', side='top')

        self.frame1 = Frame(self)
        self.frame1.config(bg='white')
        self.frame1.pack(side='top', fill='x')

        self.frame2 = Frame(self)
        self.frame2.config(bg='lightblue')
        self.frame2.pack(side='right', fill='y')

        self.frame3 = Frame(self)
        self.frame3.config(bg='white')
        self.frame3.pack(side='bottom', fill='both')

        self.frame4 = Frame(self)
        self.frame4.config(bg='white')
        self.frame4.pack(side='top', fill='x')

        self.check_btn1 = Checkbutton(self.frame2, text="Дебит нефти", variable=self.graph_oil,
                                      padx=5, pady=5,
                                      bg='lightblue')
        self.check_btn1.grid(column=0, row=0, sticky='w')

        self.check_btn2 = Checkbutton(self.frame2, text="Дебит газа", variable=self.graph_gas,
                                      padx=5, pady=5,
                                      bg='lightblue')
        self.check_btn2.grid(column=0, row=1, sticky='w')

        self.check_btn3 = Checkbutton(self.frame2, text="Дебит жидкости", variable=self.graph_water,
                                      padx=5,
                                      pady=5,
                                      bg='lightblue')
        self.check_btn3.grid(column=0, row=2, sticky='w')

        self.check_btn4 = Checkbutton(self.frame2, text="ГФ", variable=self.graph_gf, padx=5,
                                      pady=5,
                                      bg='lightblue')
        self.check_btn4.grid(column=0, row=3, sticky='w')

        self.check_btn5 = Checkbutton(self.frame2, text='Давление', variable=self.graph_pressure,
                                      padx=5, pady=5, bg='lightblue')
        self.check_btn5.grid(column=0, row=4, sticky='w')

        self.check_btn6 = Checkbutton(self.frame2, text="Обводненность", variable=self.graph_water_cut,

                                      padx=5, pady=5, bg='lightblue')
        self.check_btn6.grid(column=0, row=5, sticky='w')

        self.btn5 = Button(self.frame2, text="Построить график", command=self.Graphic, font="Arial 10", bg='white',
                           width=15)
        self.btn5.grid(column=0, row=7, padx=5, pady=5)

        self.btn6 = Button(self.frame2, text="Сравнить графики", command=self.Graphics, font="Arial 10", bg='white',
                           width=15)
        self.btn6.grid(column=0, row=8, padx=5, pady=5)

        self.txt1 = Entry(self.frame2, width=20, font="Arial 10", justify='center', bg='white')
        self.txt1.grid(column=0, row=9, padx=5, pady=5)

        self.txt2 = Entry(self.frame2, width=20, font="Arial 10", justify='center', bg='white')
        self.txt2.grid(column=0, row=10, padx=5, pady=5)

        self.lbl3 = Label(self.frame2, text='Прореживание значений', bg='lightblue')
        self.lbl3.grid(column=0, row=11, padx=5, pady=5)

        self.btn8 = Button(self.frame2, text="Каждые n", command=lambda: self.Thining(int(self.txt3.get())),
                           font="Arial 10", width=15, bg='white')
        self.btn8.grid(column=0, row=12, padx=5, pady=5)

        self.txt3 = Entry(self.frame2, width=20, font="Arial 10", justify='center', bg='white')
        self.txt3.grid(column=0, row=13, padx=5, pady=5)

        self.btn10 = Button(self.frame2, text="Логарифмически", command=lambda: self.Logarithmic(int(self.txt6.get())),
                            font="Arial 10", width=15, bg='white')
        self.btn10.grid(column=0, row=14, padx=5, pady=5)

        self.txt6 = Entry(self.frame2, width=20, font="Arial 10", justify='center', bg='white')
        self.txt6.grid(column=0, row=15, padx=5, pady=5)

        self.lbl4 = Label(self.frame2, text='Удаление значений', bg='lightblue')
        self.lbl4.grid(column=0, row=16, padx=5, pady=5)

        self.txt4 = Entry(self.frame2, width=20, font="Arial 10", justify='center', bg='white')
        self.txt4.grid(column=0, row=17, padx=5, pady=5)

        self.txt5 = Entry(self.frame2, width=20, font="Arial 10", justify='center', bg='white')
        self.txt5.grid(column=0, row=18, padx=5, pady=5)

        self.btn9 = Button(self.frame2, text="Удалить", command=self.Delete,
                           font="Arial 10", width=15, bg='white')
        self.btn9.grid(column=0, row=19, padx=5, pady=5)

        self.lbl5 = Label(self.frame2, text='Уровень сглаживания', bg='lightblue')
        self.lbl5.grid(column=0, row=20, padx=5, pady=5)

        self.scale = Scale(self.frame2, orient="horizontal", resolution=1, from_=1, to=200, length=100, bg='white')
        self.scale.grid(column=0, row=21, padx=5, pady=5)

    def Download_file(self):
        download = Download(self)
        download.tkraise(self)

    def Method_dbscan(self):
        self.lbl2.config(text=f'DBscan')

        self.frame1.destroy()
        self.frame3.destroy()
        self.frame4.destroy()

        self.frame1 = Frame(self)
        self.frame1.config(bg='lightblue')
        self.frame1.pack(side='top', padx=200)

        self.frame4 = Frame(self)
        self.frame4.config(bg='lightblue')
        self.frame4.pack(side='top', padx=200)

        btn2 = Button(self.frame1, text="K-distances graph", font="Arial 10",
                      command=lambda: self.Epsilon(int(txt2.get())), bg='white', width=15)
        btn2.pack(side='right', padx=5, pady=5)

        btn1 = Button(self.frame1, text="DBscan", command=lambda: self.DBscan(float(txt1.get()), int(txt2.get())),
                      font="Arial 10", bg='white', width=15)
        btn1.pack(side='right', padx=5, pady=5)

        txt2 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt2.pack(side='right', padx=5, pady=5)
        txt2.insert(0, '6')

        lbl2 = Label(self.frame1, text='MinElements:', font="Arial 10", bg='lightblue')
        lbl2.pack(side='right', padx=5, pady=5)

        txt1 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt1.pack(side='right', padx=5, pady=5)
        txt1.insert(0, '0.1')

        lbl1 = Label(self.frame1, text='Eps:', font="Arial 10", bg='lightblue')
        lbl1.pack(side='right', padx=5, pady=5)

        btn2 = Radiobutton(self.frame4, text="Автоматически", variable=self.dbscan_mode,
                           value=1,
                           font="Arial 10", bg='lightblue',
                           width=12)
        btn2.pack(side='right', padx=5, pady=5)

        btn3 = Radiobutton(self.frame4, text="Вручную", variable=self.dbscan_mode, value=0,
                           font="Arial 10", bg='lightblue',
                           width=12)
        btn3.pack(side='right', padx=5, pady=5)

        self.Graphic()

    def Method_isolation_forest(self):
        self.lbl2.config(text=f'IsolationForest')

        self.frame1.destroy()
        self.frame3.destroy()
        self.frame4.destroy()

        self.frame1 = Frame(self)
        self.frame1.config(bg='lightblue')
        self.frame1.pack(side='top')

        self.frame4 = Frame(self)
        self.frame4.config(bg='lightblue')
        self.frame4.pack(side='top', padx=200)

        btn1 = Button(self.frame1, text="IsolationForest", command=lambda: self.IsolationForest(float(txt1.get())),
                      font="Arial 10", bg='white', width=15)
        btn1.pack(side='right', padx=5, pady=5)

        txt1 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt1.pack(side='right', padx=5, pady=5)
        txt1.insert(0, '0.1')

        lbl1 = Label(self.frame1, text='Сontamination:', font="Arial 10", bg='lightblue')
        lbl1.pack(side='right', padx=5, pady=5)

        self.Graphic()

    def Method_local_outlier_factor(self):
        self.lbl2.config(text=f'LocalOutlierFactor')

        self.frame1.destroy()
        self.frame3.destroy()
        self.frame4.destroy()

        self.frame1 = Frame(self)
        self.frame1.config(bg='lightblue')
        self.frame1.pack(side='top')

        self.frame4 = Frame(self)
        self.frame4.config(bg='lightblue')
        self.frame4.pack(side='top', padx=200)

        btn1 = Button(self.frame1, text="LocalOutlierFactor",
                      command=lambda: self.LocalOutlierFactor(int(txt2.get()), float(txt1.get())),
                      font="Arial 10", bg='white', width=15)
        btn1.pack(side='right', padx=5, pady=5)

        txt1 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt1.pack(side='right', padx=5, pady=5)
        txt1.insert(0, '0.1')

        lbl1 = Label(self.frame1, text='Сontamination:', font="Arial 10", bg='lightblue')
        lbl1.pack(side='right', padx=5, pady=5)

        txt2 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt2.pack(side='right', padx=5, pady=5)
        txt2.insert(0, '20')

        lbl2 = Label(self.frame1, text='Neighbors:', font="Arial 10", bg='lightblue')
        lbl2.pack(side='right', padx=5, pady=5)

        self.Graphic()

    def Method_Z_score(self):
        self.lbl2.config(text=f'Z-score')

        self.frame1.destroy()
        self.frame3.destroy()
        self.frame4.destroy()

        self.frame1 = Frame(self)
        self.frame1.config(bg='lightblue')
        self.frame1.pack(side='top')

        self.frame4 = Frame(self)
        self.frame4.config(bg='lightblue')
        self.frame4.pack(side='top', padx=200)

        btn1 = Button(self.frame1, text="Z-score",
                      command=lambda: self.Zscore(float(txt1.get())),
                      font="Arial 10", bg='white', width=15)
        btn1.pack(side='right', padx=5, pady=5)

        txt1 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt1.pack(side='right', padx=5, pady=5)
        txt1.insert(0, '2')

        lbl1 = Label(self.frame1, text='Score:', font="Arial 10", bg='lightblue')
        lbl1.pack(side='right', padx=5, pady=5)

        self.Graphic()

    def Method_MA(self):
        self.lbl2.config(text=f'MA')

        self.frame1.destroy()
        self.frame3.destroy()
        self.frame4.destroy()

        self.frame1 = Frame(self)
        self.frame1.config(bg='lightblue')
        self.frame1.pack(side='top')

        self.frame4 = Frame(self)
        self.frame4.config(bg='lightblue')
        self.frame4.pack(side='top', padx=200)

        btn1 = Button(self.frame1, text="MA",
                      command=lambda: self.MA(float(txt1.get()), int(txt2.get())),
                      font="Arial 10", bg='white', width=15)
        btn1.pack(side='right', padx=5, pady=5)

        txt1 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt1.pack(side='right', padx=5, pady=5)
        txt1.insert(0, '2')

        lbl1 = Label(self.frame1, text='Score:', font="Arial 10", bg='lightblue')
        lbl1.pack(side='right', padx=5, pady=5)

        txt2 = Entry(self.frame1, width=10, font="Arial 10", justify='center', bg='white')
        txt2.pack(side='right', padx=5, pady=5)
        txt2.insert(0, '60')

        lbl2 = Label(self.frame1, text='Window:', font="Arial 10", bg='lightblue')
        lbl2.pack(side='right', padx=5, pady=5)

        self.Graphic()

    def DBscan_hand(self, eps, elements):
        self.borehole.Standard()
        self.borehole_list.append(self.borehole.df.copy(deep=True))

        dbscan = DBSCAN(eps=eps, min_samples=elements).fit(self.borehole.x_scaled)
        self.borehole.df['Cluster'] = dbscan.labels_
        self.Graphic()

    def DBscan_auto(self, elements):
        self.borehole.Standard()
        nbrs = NearestNeighbors(n_neighbors=elements).fit(self.borehole.x_scaled)
        distances, indices = nbrs.kneighbors(self.borehole.x_scaled)
        distances = np.sort(distances[:, 1:].mean(axis=1))
        dist_prime = distances[1:] - distances[:-1]
        self.DBscan_hand(distances[np.argmax(dist_prime[1:] - dist_prime[:-1]) - 20], elements)
        time.sleep(1)
        self.Remove()

    def DBscan(self, eps, elements):
        if self.dbscan_mode.get():
            self.DBscan_auto(elements)
        else:
            self.DBscan_hand(eps, elements)

    def IsolationForest(self, cont):
        self.borehole.Standard()
        self.borehole_list.append(self.borehole.df.copy(deep=True))

        graph = [self.graph_water.get(), self.graph_gas.get(), self.graph_water_cut.get(), self.graph_oil.get(),
                 self.graph_gf.get(),
                 self.graph_pressure.get()]
        forest = IsolationForest(n_estimators=1000, contamination=cont, max_features=sum(graph),
                                 random_state=42, bootstrap=True).fit_predict(
            self.borehole.x_scaled.iloc[:, [i for i, v in enumerate(graph) if v == 1]].values)
        self.borehole.df['Cluster'] = forest
        self.Graphic()

    def LocalOutlierFactor(self, neighbors, cont):
        self.borehole.Standard()
        self.borehole_list.append(self.borehole.df.copy(deep=True))

        local = LocalOutlierFactor(n_neighbors=neighbors, contamination=cont).fit_predict(self.borehole.x_scaled)
        self.borehole.df['Cluster'] = local
        self.Graphic()

    def Zscore(self, score):
        self.borehole.Standard()
        self.borehole_list.append(self.borehole.df.copy(deep=True))
        graph = [self.graph_water.get(), self.graph_gas.get(), self.graph_water_cut.get(), self.graph_oil.get(),
                 self.graph_gf.get(),
                 self.graph_pressure.get()]
        z = np.abs(stats.zscore(self.borehole.df.iloc[:, [i for i, v in enumerate(graph) if v == 1]].values))
        self.borehole.df.loc[
            self.borehole.df.index.isin(
                self.borehole.df.iloc[list(np.where(z > score)[0])].index.tolist()), 'Cluster'] = -1
        self.borehole.df.loc[
            ~self.borehole.df.index.isin(
                self.borehole.df.iloc[list(np.where(z > score)[0])].index.tolist()), 'Cluster'] = 1

        self.Graphic()

    def IQR(self):
        self.borehole.Standard()
        self.borehole_list.append(self.borehole.df.copy(deep=True))
        graph = [self.graph_water.get(), self.graph_gas.get(), self.graph_water_cut.get(), self.graph_oil.get(),
                 self.graph_gf.get(),
                 self.graph_pressure.get()]
        for column in self.borehole.df.iloc[:, [i for i, v in enumerate(graph) if v == 1]]:
            q75, q25 = np.percentile(self.borehole.df.loc[:, column], [75, 25])
            inter_qr = q75 - q25

            max_value = q75 + (1.5 * inter_qr)
            min_value = q25 - (1.5 * inter_qr)
            self.borehole.df.loc[self.borehole.df[column] < min_value, 'CLuster'] = -1
            self.borehole.df.loc[self.borehole.df[column] > max_value, 'Cluster'] = -1
        self.Graphic()

    def MA(self, score, window):
        pd.set_option('display.max_rows', None)
        self.borehole.Standard()
        self.borehole_list.append(self.borehole.df.copy(deep=True))
        graph = [self.graph_water.get(), self.graph_gas.get(), self.graph_water_cut.get(), self.graph_oil.get(),
                 self.graph_gf.get(),
                 self.graph_pressure.get()]
        df = self.borehole.df.iloc[:, [i for i, v in enumerate(graph) if v == 1]]
        df_mean = self.borehole.df.iloc[:, [i for i, v in enumerate(graph) if v == 1]].rolling(window=window,
                                                                                               center=True,
                                                                                               min_periods=1).mean()
        df_std = self.borehole.df.iloc[:, [i for i, v in enumerate(graph) if v == 1]].rolling(window=window,
                                                                                              center=True,
                                                                                              min_periods=1).std()
        df_low_pass_filter_anomaly = (abs(df - df_mean) > (score * df_std))
        df_low_pass_filter_anomaly = df_low_pass_filter_anomaly.replace({True: -1, False: 1})
        self.borehole.df['Cluster'] = df_low_pass_filter_anomaly

        self.Graphic()

    def Color(self):
        stake_color = len(set(self.borehole.df['Cluster'])) * ['black']
        stake_cluster = set(self.borehole.df['Cluster'])
        clusterColor = dict(zip(stake_cluster, stake_color))
        clusterColor[-1] = 'red'
        return [clusterColor[label] for label in self.borehole.df['Cluster']]

    def Epsilon(self, k):
        self.borehole.Standard()
        self.frame3.destroy()

        self.frame3 = Frame(self)
        self.frame3.config(bg='white')
        self.frame3.pack(side='bottom', fill='both')

        nbrs = NearestNeighbors(n_neighbors=k).fit(self.borehole.x_scaled)
        distances, indices = nbrs.kneighbors(self.borehole.x_scaled)
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
        plt.close(fig)

        graph = [self.graph_oil.get(), self.graph_gas.get(), self.graph_water.get(), self.graph_gf.get(),
                 self.graph_pressure.get(), self.graph_water_cut.get()]
        parametr = [self.borehole.param[6], self.borehole.param[3], self.borehole.param[2], self.borehole.param[10],
                    self.borehole.param[self.borehole.pressure], self.borehole.param[4]]
        if 1 in graph:
            ax = fig.add_subplot()
            if self.graphic_mode.get() == 1:
                ax.scatter(self.borehole.df.index.tolist(), self.borehole.df[parametr[graph.index(1)]], s=6,
                           c=self.Color())
            elif self.graphic_mode.get() == 2:
                x = np.arange(len(self.borehole.df.index.tolist()))
                y = np.array(self.borehole.df[parametr[graph.index(1)]].tolist())
                d = [1 / std(y)] * len(x)
                tck = splrep(x, y, w=d, s=self.scale.get(), k=3)
                spl = splev(x, tck)
                ax.scatter(self.borehole.df.index.tolist(), y, s=6,
                           c=self.Color())
                ax.plot(self.borehole.df.index.tolist(),
                        self.borehole.df[parametr[graph.index(1)]].rolling(window=self.scale.get(),
                                                                           center=True,
                                                                           min_periods=1).mean(),
                        color='orange',
                        linewidth=2,
                        linestyle='-')
            else:
                x = np.arange(len(self.borehole.df.index.tolist()))
                y = np.array(self.borehole.df[parametr[graph.index(1)]].tolist())
                d = [1 / std(y)] * len(x)
                tck = splrep(x, y, w=d, s=self.scale.get(), k=3)
                spl = splev(x, tck)
                ax.plot(self.borehole.df.index.tolist(),
                        self.borehole.df[parametr[graph.index(1)]].rolling(window=self.scale.get(),
                                                                           center=True,
                                                                           min_periods=1).mean(),
                        color='orange',
                        linewidth=2,
                        linestyle='-')
            ax.set(ylabel=f'{parametr[graph.index(1)]}')
            ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        toolbar = NavigationToolbar2Tk(canvas, self.frame3)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.update_idletasks()

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
            if self.graphic_mode.get() == 1:
                ax1.scatter(self.borehole.df.index.tolist(), self.borehole.df[parametr[graph.index(1)]], s=6,
                            c=self.Color())
            elif self.graphic_mode.get() == 2:
                x = np.arange(len(self.borehole.df.index.tolist()))
                y = np.array(self.borehole.df[parametr[graph.index(1)]].tolist())
                d = [1 / std(y)] * len(x)
                tck = splrep(x, y, w=d, s=self.scale.get(), k=3)
                spl = splev(x, tck)
                ax1.scatter(self.borehole.df.index.tolist(), y, s=3,
                            c=self.Color())
                ax1.plot(self.borehole.df.index.tolist(), spl, color='orange',
                         linewidth=2,
                         linestyle='-')
            else:
                x = np.arange(len(self.borehole.df.index.tolist()))
                y = np.array(self.borehole.df[parametr[graph.index(1)]].tolist())
                d = [1 / std(y)] * len(x)
                tck = splrep(x, y, w=d, s=self.scale.get(), k=3)
                spl = splev(x, tck)
                ax1.plot(self.borehole.df.index.tolist(), spl, color='orange',
                         linewidth=2,
                         linestyle='-')
            ax1.set(ylabel=f'{parametr[graph.index(1)]}')
            ax1.grid(True)
            graph[graph.index(1)] = 0
            if 1 in graph:
                ax2 = fig.add_subplot(2, 1, 2)
                if self.graphic_mode.get() == 1:
                    ax2.scatter(self.borehole.df.index.tolist(), self.borehole.df[parametr[graph.index(1)]], s=6,
                                c=self.Color())
                elif self.graphic_mode.get() == 2:
                    x = np.arange(len(self.borehole.df.index.tolist()))
                    y = np.array(self.borehole.df[parametr[graph.index(1)]].tolist())
                    d = [1 / std(y)] * len(x)
                    tck = splrep(x, y, w=d, s=self.scale.get(), k=3)
                    spl = splev(x, tck)
                    ax2.scatter(self.borehole.df.index.tolist(), y, s=3,
                                c=self.Color())
                    ax2.plot(self.borehole.df.index.tolist(), spl, color='orange',
                             linewidth=2,
                             linestyle='-')
                else:
                    x = np.arange(len(self.borehole.df.index.tolist()))
                    y = np.array(self.borehole.df[parametr[graph.index(1)]].tolist())
                    d = [1 / std(y)] * len(x)
                    tck = splrep(x, y, w=d, s=self.scale.get(), k=3)
                    spl = splev(x, tck)
                    ax2.plot(self.borehole.df.index.tolist(), spl, color='orange',
                             linewidth=2,
                             linestyle='-')
                ax2.set(ylabel=f'{parametr[graph.index(1)]}')
                ax2.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        toolbar = NavigationToolbar2Tk(canvas, self.frame3)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.update_idletasks()

    def Part(self):
        self.borehole_list.append(self.borehole.df.copy(deep=True))
        if self.borehole.df.index.tolist() != self.borehole_copy.df.index.tolist():
            self.borehole_copy.df = self.borehole_copy.df.append(self.borehole.df)
            self.borehole_copy.df.sort_index(inplace=True)
            self.borehole.df = self.borehole_copy.df.copy(deep=True)
        self.borehole.df = self.borehole.df.loc[self.txt1.get():self.txt2.get(), :]
        self.borehole_copy.df = self.borehole_copy.df[
            ~self.borehole_copy.df.index.isin(self.borehole.df.index.tolist())]
        self.Entry_date()
        self.Graphic()
        print(self.borehole.df[self.borehole.df['Cluster'] == -1])

    def All(self):
        self.borehole_list.append(self.borehole.df.copy(deep=True))
        self.borehole_copy.df = self.borehole_copy.df.append(self.borehole.df)
        self.borehole_copy.df.sort_index(inplace=True)
        self.borehole.df = self.borehole_copy.df.copy(deep=True)
        self.Entry_date()
        self.Graphic()

    def Remove(self):
        if self.borehole.df['Cluster'].isin([-1]).any():
            self.borehole_list.append(self.borehole.df.copy(deep=True))
        if self.borehole.df.index.tolist() != self.borehole_copy.df.index.tolist():
            self.borehole.df = self.borehole.df.loc[self.borehole.df['Cluster'] != -1]
            self.borehole_copy.df = self.borehole_copy.df.append(self.borehole.df)
            self.borehole_copy.df.sort_index(inplace=True)
            self.borehole_copy.df = self.borehole_copy.df[
                ~self.borehole_copy.df.index.isin(self.borehole.df.index.tolist())]
        else:
            self.borehole.df = self.borehole.df.loc[self.borehole.df['Cluster'] != -1]
            self.borehole_copy.df = self.borehole_copy.df.loc[self.borehole.df.index]
        self.Entry_date()
        self.Graphic()

    def Writer(self):
        with pd.ExcelWriter("Two.xlsx", mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            self.borehole.df.iloc[:, :-1].to_excel(writer, sheet_name=f'{self.borehole.name}')

    def Cancel(self):
        try:
            self.borehole_copy.df = self.borehole_copy.df.append(self.borehole.df)
            self.borehole_copy.df.sort_index(inplace=True)
            self.borehole.df = self.borehole_list[-1]
            self.borehole_list.pop(-1)
            if self.borehole.df.index[0] == self.borehole_copy.df.index[0] and self.borehole.df.index[-1] == \
                    self.borehole_copy.df.index[-1]:
                self.data_part.set(value=1)
            self.Entry_date()
            self.Graphic()
        except IndexError:
            messagebox.showinfo("Information", "Исходные данные")

    def Thining(self, n):
        self.borehole_list.append(self.borehole.df.copy(deep=True))
        self.borehole.df = self.borehole.df[~self.borehole.df.index.isin(self.borehole.df.iloc[::n].index.tolist())]
        self.Entry_date()
        self.Graphic()

    def Logarithmic(self, n):
        self.borehole_list.append(self.borehole.df.copy(deep=True))
        i = n
        thining_list = []
        while i < self.borehole.df.shape[0]:
            thining_list.append(i)
            i += round(n * np.log(i))
        print(thining_list)
        self.borehole.df = self.borehole.df[~self.borehole.df.index.isin([self.borehole.df.index.tolist()[j] for j in thining_list])]
        self.Entry_date()
        self.Graphic()

    def Entry_date(self):
        self.txt1.delete(0, END)
        self.txt2.delete(0, END)
        self.txt1.insert(0, self.borehole.df.index[0])
        self.txt2.insert(0, self.borehole.df.index[-1])

        self.txt4.delete(0, END)
        self.txt5.delete(0, END)
        self.txt4.insert(0, self.borehole.df.index[0])
        self.txt5.insert(0, self.borehole.df.index[0])

    def Delete(self):
        self.borehole_list.append(self.borehole.df.copy(deep=True))
        self.borehole.df = self.borehole.df[
            ~self.borehole.df.index.isin(self.borehole.df.loc[self.txt4.get():self.txt5.get(), :].index.tolist())]

        self.Entry_date()
        self.Graphic()


if __name__ == '__main__':
    widget = Widget()
    widget.Download_file()
    widget.mainloop()
