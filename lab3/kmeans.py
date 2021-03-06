import pandas as pd
import numpy as np
from copy import deepcopy
from random import sample

def distance(v1, v2, ax=1):
    return np.linalg.norm(v1 - v2, axis=ax) #узнаем расстояние между точками и центроидами


class KMeans:
    def __init__(self, n_clusters, max_iter=300):
        self.n_clusters = n_clusters
        self.max_iter = max_iter

    def fit(self, X):
        n_samples = len(X)
        centroids = X[np.random.choice(X.shape[0], self.n_clusters, replace=False)]  # выбираем центроиды рандомно, X.shape[0] - строки
        centroids_old = np.zeros(centroids.shape)   # .shape - размер массива (длина массива по каждой оси)
        clusters = np.zeros(n_samples)  # матрица из нулей размером Х

        while True:
            for i in range(n_samples):
                distances = distance(X[i,], centroids)
                clusters[i] = distances.argmin()    # min разница между центроидом и элементами
            centroids_old = deepcopy(centroids)  # копируем координаты центроидов, чтобы потом выбрать наилучшие
            for k in range(self.n_clusters):
                centroids[k] = X[clusters == k,].mean(axis=0)   # определяем каждый центроид к какому-нибудь кластеру
            error = distance(centroids, centroids_old, None)    # центроид перестаёт двигаться => он определён верно
            if (error >= 0) and (error <= 0.01):
                self.clusters = clusters.astype('int')  # принадлежность элемента к тому или иному кластеру
                self.centroids = centroids  # центроиды
                break

    def predict(self, y):
        """
        Считаем центроиды по принадлежности к кластеру
        :param y: принадлежность элемента к кластеру
        :return: центроиды, принадлежность
        """
        y_unique = np.unique(y)  # выделяем кластеры
        y_unique_num = [i for i in range(len(np.unique(y)))]    # номера для кластеров
        n_samples = len(X)
        clusters = np.zeros(n_samples)  # матрица из нулей размером Х
        for k in range(n_samples): #кластерам присваиваются цифры вместо названий
            for j in range(self.n_clusters):
                if y[k][0] == y_unique[j]:
                    y[k] = y_unique_num[j]
            clusters[k] = y[k]
        centroids = X[np.random.choice(X.shape[0], self.n_clusters,
                                       replace=False)]  # рандомно выбираем место центроидов, X.shape[0] - строки
        centroids_old = np.zeros(centroids.shape)  # .shape - размер массива (длина массива по каждой оси)
        while True:
            centroids_old = deepcopy(centroids)  # копируем координаты центроидов, чтобы потом выбрать наилучшие
            error = distance(centroids, centroids_old, None)    # случай, когда центроид перестаёт двигаться, соответственно, он определён верно
            if error == 0:
                self.clusters = clusters.astype(int)
                self.centroids = centroids
                return self.centroids, self.clusters

if __name__ == '__main__':
    data = pd.read_csv('iris.csv')
    model = KMeans(3)
    X = (data.loc[:, data.columns != 'Name']).as_matrix() # берется выборка
    y = (data.loc[:, data.columns == 'Name']).as_matrix()
    model.fit(X)
    print(model.predict(y))
