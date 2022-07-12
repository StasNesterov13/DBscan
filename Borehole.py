import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as palette
from openpyxl import load_workbook
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


class Borehole:

    def __init__(self):
        self.df = pd.DataFrame()
        self.name = None
        self.x_principal = None
        self.x_scaled = None
        self.param = ['Состояние', 'Dшт, мм', 'Qж, м3/сут', 'Qгаз, м3/сут', 'Обв, %', 'Обв ХАЛ, %', 'Qн, т/сут',
                      'Рбуф, атм', 'Рзатр, атм', 'Рлин, атм', 'ГФ, м3/т', 'Рпл ГНК', 'Рзаб ГНК', 'F, Гц', 'Рприем, атм',
                      'Прим', 'Рзаб замер', 'Траб']

    def Creature(self, start, end, num_data):
        wb = load_workbook(filename='Debit.xlsx', read_only=True, data_only=True)
        ws = wb[f'{wb.sheetnames[0]}']
        time = []
        data = []
        for row in ws[f'{start}2':f'{end}2']:
            for cell in row:
                time.append(cell.value)
        for i in [num_data + 2, num_data + 3, num_data + 4, num_data + 6,
                  num_data + 10, num_data + 12]:
            data_row = []
            for row in ws[f'{start}{i}':f'{end}{i}']:
                for cell in row:
                    data_row.append(cell.value)
                    print(cell.value)
            data.append(data_row)

        self.name = ws[f'A{num_data}'].value
        self.df = pd.DataFrame(data, index=[self.param[2], self.param[3], self.param[4], self.param[6], self.param[10],
                                            self.param[12]], columns=time)
        self.df = self.df.transpose()
        self.df.dropna(axis=0, how='all', inplace=True)
        self.df.fillna(value=0, inplace=True)
        for cell in set(self.df.index.tolist()):
            if isinstance(cell, str):
                self.df.drop(index=cell, inplace=True)
        wb.close()

        writer = pd.ExcelWriter('One.xlsx')
        self.df.to_excel(writer)
        writer.save()

        wb = load_workbook(filename='One.xlsx')
        wb[f'{wb.sheetnames[0]}']['A1'].value = self.name
        wb.save(filename='One.xlsx')
        wb.close()

        self.Standard()

    def Read(self):
        wb = load_workbook(filename='One.xlsx', read_only=True)
        self.name = wb[f'{wb.sheetnames[0]}']['A1'].value
        self.df = pd.read_excel('One.xlsx', sheet_name=f'{wb.sheetnames[0]}', index_col=0)
        self.Standard()
        wb.close()

    def Standard(self):

        self.df['Cluster'] = 0

        self.x_scaled = StandardScaler().fit_transform(self.df)

        self.x_principal = PCA(n_components=2).fit_transform(self.x_scaled)
        self.x_principal = pd.DataFrame(self.x_principal)
        self.x_principal.columns = ['V1', 'V2']

    def Epsilon(self, k):
        nbrs = NearestNeighbors(n_neighbors=k).fit(self.x_principal)
        distances, indices = nbrs.kneighbors(self.x_principal)
        distances = np.sort(distances[:, 1:].mean(axis=1))
        plt.figure(figsize=(10, 5))
        plt.plot(distances)
        plt.title('K-distance Graph', fontsize=10)
        plt.xlabel('Data Points sorted by distance', fontsize=7)
        plt.ylabel('Epsilon', fontsize=7)
        plt.grid(True)
        plt.show()

    def Scan(self, eps, elements):
        dbscan = DBSCAN(eps=eps, min_samples=elements).fit(self.x_principal)
        labels = dbscan.labels_
        self.df['Cluster'] = labels

    def Color(self):
        stake = ['black'] + list(palette.CSS4_COLORS.values())[10:] + ['red']
        clusterColor = {}

        for i in range(-1, len(set(self.df['Cluster']))):
            clusterColor[i] = stake[i]

        return [clusterColor[label] for label in self.df['Cluster']]

    def Clustering(self):
        plt.figure(figsize=(10, 8))
        plt.scatter(self.x_principal['V1'], self.x_principal['V2'], s=15, c=self.Color())
        plt.title('Implementation of DBSCAN Clustering', fontname='Times New Roman', fontweight='bold')
        plt.show()

    def Graphics_oil(self):
        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[6]], s=15, c=self.Color())
        plt.title('Qн, т/сут', fontname='Times New Roman', fontweight='bold')
        plt.grid(True)
        plt.show()

    def Graphics_gas(self):
        color = []
        for label in self.df['Cluster']:
            if label == -1:
                color.append('red')
            else:
                color.append('black')

        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[3]], s=15, c=color)
        plt.title('Qгаз, м3/сут', fontname='Times New Roman', fontweight='bold')
        plt.grid(True)
        plt.show()

    def Graphics_water(self):
        color = []
        for label in self.df['Cluster']:
            if label == -1:
                color.append('red')
            else:
                color.append('black')

        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[4]], s=15, c=color)
        plt.title('Обв, %', fontname='Times New Roman', fontweight='bold')
        plt.grid(True)
        plt.show()

    def Graphics_gf(self):
        color = []
        for label in self.df['Cluster']:
            if label == -1:
                color.append('red')
            else:
                color.append('black')

        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[10]], s=15, c=color)
        plt.title('ГФ, м3/т', fontname='Times New Roman', fontweight='bold')
        plt.grid(True)
        plt.show()

    def Graphics_pressure(self):
        color = []
        for label in self.df['Cluster']:
            if label == -1:
                color.append('red')
            else:
                color.append('black')

        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[12]], s=15, c=color)
        plt.title('Рзаб ГНК', fontname="Times New Roman", fontweight="bold")
        plt.grid(True)
        plt.show()

    def Remove(self):
        self.df = self.df.loc[self.df['Cluster'] != -1]
        self.Standard()

    def Writer(self):
        writer = pd.ExcelWriter('Two.xlsx')
        self.df.to_excel(writer)
        writer.save()
