import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize


class Borehole:

    def __init__(self, start='E', end='BNQ', num_data=3):
        self.col_start = start
        self.col_end = end
        self.number_data = int(num_data)
        self.df = pd.DataFrame()
        self.param = ['Состояние', 'Dшт, мм', 'Qж, м3/сут', 'Qгаз, м3/сут', 'Обв, %', 'Обв ХАЛ, %', 'Qн, т/сут',
                      'Рбуф, атм', 'Рзатр, атм', 'Рлин, атм', 'ГФ, м3/т', 'Рпл ГНК', 'Рзаб ГНК', 'F, Гц', 'Рприем, атм',
                      'Прим', 'Рзаб замер', 'Траб']

    def Creature(self):
        wb = load_workbook(filename='Debit.xlsx', read_only=True, data_only=True)
        ws = wb['1']
        time = []
        data = []
        for row in ws[self.col_start + '2':self.col_end + '2']:
            for cell in row:
                time.append(cell.value)
        for i in [self.number_data + 2, self.number_data + 3, self.number_data + 4, self.number_data + 6,
                  self.number_data + 10, self.number_data + 12]:
            data_row = []
            for row in ws[self.col_start + str(i):self.col_end + str(i)]:
                for cell in row:
                    data_row.append(cell.value)
                    print(cell.value)
            data.append(data_row)
        self.df = pd.DataFrame(data, index=[self.param[2], self.param[3], self.param[4], self.param[6], self.param[10],
                                            self.param[12]], columns=time)
        self.df = self.df.transpose()
        self.df.dropna(axis=0, how='any', inplace=True)
        wb.close()

        import os
        os.remove('One.xlsx')

        writer = pd.ExcelWriter('One.xlsx')
        self.df.to_excel(writer)
        writer.save()

        wb = load_workbook(filename='One.xlsx')
        wb['Sheet1']['A1'].value = self.number_data
        wb.save(filename='One.xlsx')
        wb.close()

    def Read(self):
        wb = load_workbook(filename='One.xlsx', read_only=True)
        self.number_data = wb['Sheet1']['A1'].value
        self.df = pd.read_excel('One.xlsx', sheet_name='Sheet1', index_col=0)
        self.Standard()
        self.df['Cluster'] = 0
        print(self.df)

    def Standard(self):
        sc = StandardScaler()
        x_scaled = sc.fit_transform(self.df)

        x_normal = normalize(x_scaled)
        x_normal = pd.DataFrame(x_normal)

        pca = PCA(n_components=2)
        global x_principal
        x_principal = pca.fit_transform(x_normal)
        x_principal = pd.DataFrame(x_principal)
        x_principal.columns = ['V1', 'V2']

    @staticmethod
    def Epsilon():
        nbrs = NearestNeighbors(n_neighbors=2).fit(x_principal)
        distances, indices = nbrs.kneighbors(x_principal)
        distances = np.sort(distances, axis=0)
        distances = distances[:, 1]
        plt.figure(figsize=(10, 5))
        plt.plot(distances)
        plt.title('K-distance Graph', fontsize=10)
        plt.xlabel('Data Points sorted by distance', fontsize=7)
        plt.ylabel('Epsilon', fontsize=7)
        plt.grid(True)
        plt.show()

    def Scan(self, eps, elements):
        dbscan = DBSCAN(eps=eps, min_samples=elements).fit(x_principal)
        labels = dbscan.labels_
        self.df['Cluster'] = labels

    def Clustering(self):
        import matplotlib.colors as palette

        stake = list(palette.CSS4_COLORS.values())[10:] + ['red']
        clusterColor = {}

        for i in range(-1, len(set(self.df['Cluster']))):
            clusterColor[i] = stake[i]

        color = [clusterColor[label] for label in self.df['Cluster']]
        plt.figure(figsize=(10, 8))
        plt.scatter(x_principal['V1'], x_principal['V2'], s=15, c=color)
        plt.title("Implementation of DBSCAN Clustering", fontname="Times New Roman", fontweight="bold")
        plt.show()

    def Graphics_oil(self):
        if 'Cluster' in self.df.columns.tolist():
            color = []
            for label in self.df['Cluster']:
                if label == -1:
                    color.append('red')
                else:
                    color.append('black')
        else:
            color = 'black'
        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[6]], s=15, c=color)
        plt.title("Qн, т/сут", fontname="Times New Roman", fontweight="bold")
        plt.grid(True)
        plt.show()

    def Graphics_gas(self):
        if 'Cluster' in self.df.columns.tolist():
            color = []
            for label in self.df['Cluster']:
                if label == -1:
                    color.append('red')
                else:
                    color.append('black')
        else:
            color = 'black'

        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[3]], s=15, c=color)
        plt.title("Qгаз, м3/сут", fontname="Times New Roman", fontweight="bold")
        plt.grid(True)
        plt.show()

    def Graphics_water(self):
        if 'Cluster' in self.df.columns.tolist():
            color = []
            for label in self.df['Cluster']:
                if label == -1:
                    color.append('red')
                else:
                    color.append('black')
        else:
            color = 'black'

        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[4]], s=15, c=color)
        plt.title("Обв, %", fontname="Times New Roman", fontweight="bold")
        plt.grid(True)
        plt.show()

    def Graphics_gf(self):
        if 'Cluster' in self.df.columns.tolist():
            color = []
            for label in self.df['Cluster']:
                if label == -1:
                    color.append('red')
                else:
                    color.append('black')
        else:
            color = 'black'

        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[10]], s=15, c=color)
        plt.title("ГФ, м3/т", fontname="Times New Roman", fontweight="bold")
        plt.grid(True)
        plt.show()

    def Graphics_pressure(self):
        if 'Cluster' in self.df.columns.tolist():
            color = []
            for label in self.df['Cluster']:
                if label == -1:
                    color.append('red')
                else:
                    color.append('black')
        else:
            color = 'black'

        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[12]], s=15, c=color)
        plt.title("'Рзаб ГНК'", fontname="Times New Roman", fontweight="bold")
        plt.grid(True)
        plt.show()

    def Graphics_all(self):
        self.Graphics_oil()
        self.Graphics_gas()
        self.Graphics_water()
        self.Graphics_gf()
        self.Graphics_pressure()

    def Remove(self):
        print(self.df.loc[self.df['Cluster'] == -1])
        self.df = self.df.loc[self.df['Cluster'] != -1]
        self.Standard()
