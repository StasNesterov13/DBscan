import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
        self.pressure = None
        self.param = ['Состояние', 'Dшт, мм', 'Qж, м3/сут', 'Qгаз, м3/сут', 'Обв, %', 'Обв ХАЛ, %', 'Qн, т/сут',
                      'Рбуф, атм', 'Рзатр, атм', 'Рлин, атм', 'ГФ, м3/т', 'Рпл ГНК', 'Рзаб ГНК', 'F, Гц', 'Рприем, атм',
                      'Прим', 'Рзаб замер', 'Траб']

    def Creature(self, start, end, num_data, press):
        wb = load_workbook(filename='Debit.xlsx', read_only=True, data_only=True)
        ws = wb[f'{wb.sheetnames[0]}']
        date = []
        data = []
        self.pressure = press
        for row in ws[f'{start}2':f'{end}2']:
            for cell in row:
                date.append(cell.value)
        progress = 0
        for i in [num_data + 2, num_data + 3, num_data + 4, num_data + 6,
                  num_data + 10, num_data + self.pressure]:
            progress += 100/6
            data_row = []
            for row in ws[f'{start}{i}':f'{end}{i}']:
                for cell in row:
                    data_row.append(cell.value)
            data.append(data_row)
            yield progress
        self.name = ws[f'A{num_data}'].value
        self.df = pd.DataFrame(data, index=[self.param[2], self.param[3], self.param[4], self.param[6], self.param[10],
                                            self.param[self.pressure]], columns=date)
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

        self.Read()

    def Read(self):
        wb = load_workbook(filename='One.xlsx', read_only=True)
        self.name = wb[f'{wb.sheetnames[0]}']['A1'].value
        self.pressure = self.param.index(wb[f'{wb.sheetnames[0]}']['G1'].value)
        wb.close()

        self.df = pd.read_excel('One.xlsx', sheet_name=f'{wb.sheetnames[0]}', index_col=0)

        self.Standard()

    def Standard(self):

        self.x_scaled = StandardScaler().fit_transform(self.df)

        self.x_principal = PCA(n_components=2).fit_transform(self.x_scaled)
        self.x_principal = pd.DataFrame(self.x_principal)

        self.df['Cluster'] = 0

    def Epsilon(self, k):
        nbrs = NearestNeighbors(n_neighbors=k).fit(self.x_principal)
        distances, indices = nbrs.kneighbors(self.x_principal)
        distances = np.sort(distances[:, 1:].mean(axis=1))
        plt.figure(figsize=(10, 5))
        plt.plot(distances)
        plt.title(f'{k}-distance Graph', fontsize=10)
        plt.xlabel('Data Points sorted by distance', fontsize=7)
        plt.ylabel('Epsilon', fontsize=7)
        plt.grid(True)
        plt.show()

    def DBscan(self, eps, elements):
        dbscan = DBSCAN(eps=eps, min_samples=elements).fit(self.x_principal)
        self.df['Cluster'] = dbscan.labels_

    def Color(self, rainbow):
        if rainbow:
            stake_color = list(palette.CSS4_COLORS.values())[10:]
        else:
            stake_color = len(set(self.df['Cluster'])) * ['black']
        stake_cluster = set(self.df['Cluster'])
        clusterColor = dict(zip(stake_cluster, stake_color))
        clusterColor[-1] = 'red'
        return [clusterColor[label] for label in self.df['Cluster']]

    def Clustering(self):
        plt.figure(figsize=(10, 8))
        plt.scatter(self.x_principal.iloc[:, 0], self.x_principal.iloc[:, 1], s=15, c=self.Color(0))
        plt.title('DBSCAN emissions', fontname='Times New Roman', fontweight='bold')
        plt.show()

    def Graphics_oil(self):
        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[6]], s=15, c=self.Color(0))
        plt.title(f'{self.param[6]}', fontname='Times New Roman', fontweight='bold')
        plt.grid(True)
        plt.show()

    def Graphics_gas(self):
        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[3]], s=15, c=self.Color(0))
        plt.title(f'{self.param[3]}', fontname='Times New Roman', fontweight='bold')
        plt.grid(True)
        plt.show()

    def Graphics_water(self):
        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[2]], s=15, c=self.Color(0))
        plt.title(f'{self.param[2]}', fontname='Times New Roman', fontweight='bold')
        plt.grid(True)
        plt.show()

    def Graphics_gf(self):
        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[10]], s=15, c=self.Color(0))
        plt.title(f'{self.param[10]}', fontname='Times New Roman', fontweight='bold')
        plt.grid(True)
        plt.show()

    def Graphics_pressure(self):
        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[self.pressure]], s=15, c=self.Color(0))
        plt.title(f'{self.param[self.pressure]}', fontname="Times New Roman", fontweight="bold")
        plt.grid(True)
        plt.show()

    def Graphics_water_cut(self):
        plt.figure(figsize=(10, 5))
        plt.scatter(self.df.index.tolist(), self.df[self.param[4]], s=15, c=self.Color(0))
        plt.title(f'{self.param[4]}', fontname="Times New Roman", fontweight="bold")
        plt.grid(True)
        plt.show()

    def Remove(self):
        self.df = self.df.loc[self.df['Cluster'] != -1]
        self.Standard()

    def Writer(self):
        writer = pd.ExcelWriter('Two.xlsx')
        self.df.iloc[:, :-1].to_excel(writer)
        writer.save()
