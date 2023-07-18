from Horner import *


def dist(k, df_scaled):
    nbrs = NearestNeighbors(n_neighbors=k).fit(df_scaled)
    distances, indices = nbrs.kneighbors(df_scaled)
    distances = np.sort(distances[:, 1:].mean(axis=1))
    plt.plot(distances)
    plt.show()


def DB(df_scaled):
    k = 3
    dbscan = DBSCAN(eps=0.1, min_samples=k).fit(df_scaled)
    return dbscan.labels_


def IF(df_scaled):
    forest = IsolationForest(n_estimators=1000, contamination=0.5).fit_predict(df_scaled)
    return forest


if __name__ == '__main__':
    df_solution = pd.read_excel('Solution.xlsx', sheet_name=f'120 (P1-2)', index_col=0, converters={0:float, 1: float, 2: float})
    df_solution = df_solution[
        (df_solution.iloc[:, 0] > 0) & (df_solution.iloc[:, 1] > 0)]
    df_scaled = standard(df_solution)

    df_solution['Cluster'] = IF(df_scaled)
    df_solution = df_solution[df_solution['Cluster'] == 1]

    plt.scatter(range(df_solution.shape[0]),
                df_solution.iloc[:, 0], s=10)
    plt.show()
    plt.scatter(range(df_solution.shape[0]),
                df_solution.iloc[:, 1], s=10)
    plt.show()
    plt.scatter(range(df_solution.shape[0]),
                df_solution.iloc[:, 2], s=10)
    plt.show()

    print(df_solution.mean())
    print(1 / (df_solution.mean()[1] * 4 * 3.14))
