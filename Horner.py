import random
from sympy import *
from Widget import *


def init(name):
    borehole = Borehole()
    borehole.Read_better(name)
    p = borehole.df['Рзаб замер']

    Qж = np.array(borehole.df['Qж, м3/сут'])
    Qн = np.array(borehole.df['Qн, т/сут'])
    Qг = np.array(borehole.df['Qгаз, м3/сут'])
    Qв = Qж - Qн
    Qгп = np.divide((Qг - Qн * 194), p)
    print(Qгп)
    Q = np.array(1.3 / 0.85 * Qн + Qв)

    date = borehole.df.index.tolist()
    return p, Q, date


def logarithm(number):
    s = [Q_list[k] * np.log((delta[number + 1] - delta_mod[k]) / (delta[number + 1] - delta_mod[k + 1])) for k in
         range(less(number))]
    return sum(s)


def less(val):
    for x in delta_mod:
        if val < x:
            return delta_mod.index(x) - 1


def solution(list_num):
    a = Symbol('a')
    b = Symbol('b')
    w = Symbol('w')

    equation = [
        a - b * (logarithm(i - 1) + Q[i - 1] * log(w) + Q[i - 1] * np.log(
            86400 * (delta[i] - delta_mod[less(i - 1)]))) - p[i]
        for i in list_num]
    print(equation[0])
    print(equation[1])
    print(equation[2])
    solved_value = solve([equation[0], equation[1], equation[2]], [a, b, w])
    print(solved_value)
    if solved_value:
        return solved_value[0]


def standard(df):
    df_scaled = StandardScaler().fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled)
    return df_scaled


if __name__ == '__main__':

    p, Q, date = init('120 (P1-2)')

    N_list = [0]
    Q_list = [Q[0]]
    Qo = Q[0]
    n = 0
    while Qo != Q[-1]:
        while Qo == Q[n]:
            n += 1
        Qo = Q[n]
        N_list.append(n)
        Q_list.append(Q[n])

    delta = [(date[i] - date[0]).days for i in range(len(date))]
    delta_mod = [(date[i] - date[0]).days for i in N_list]

    list_numbers = list(range(1, 150))
    list_solution = []

    for j in range(int(input())):
        random.shuffle(list_numbers)
        list_solution.append(solution(list_numbers[:3]))
    list_solution = np.array(list(filter(lambda item: item is not None, list_solution)))

    df_solution = pd.DataFrame(list_solution)
    print(df_solution)
    with pd.ExcelWriter("Solution.xlsx", mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        df_solution.to_excel(writer, sheet_name=f'120 (P1-2)')
