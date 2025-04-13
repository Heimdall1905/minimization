from tabulate import tabulate
import numpy as np


# наша функция, для которой мы ищем минимум
def f0(x, y, z):
    return 5 * (x - 15) ** 2 + 5 * (y - 3) ** 2 + 5 * (z - 19) ** 2 + 2 * (x - 15) * (y - 3) + 2 * (x - 15) * (
                z - 19) + 2 * (y - 3) * (z - 19)


# частные производные нашей функции
def X(m):
    return 10 * (m[0] - 15) + 2 * (m[1] - 3) + 2 * (m[2] - 19)


def Y(m):
    return 10 * (m[1] - 3) + 2 * (m[0] - 15) + 2 * (m[2] - 19)


def Z(m):
    return 10 * (m[2] - 19) + 2 * (m[0] - 15) + 2 * (m[1] - 3)


# градиент вектора
def grad(m):
    return np.array([X(m), Y(m), Z(m)])


# норма вектора
def norm(m):
    return np.sqrt(m[0] ** 2 + m[1] ** 2) + m[2] ** 2


def Diho(f):
    # начальные параметры метода дихотомии
    a = -100
    b = 100
    e0 = 1e-5
    v = 1e-6

    a1 = a
    b1 = b

    while (b1 - a1) > e0:

        c1 = (a1 + b1) / 2 - v / 2
        fc = f(c1)
        d1 = (a1 + b1) / 2 + v / 2
        fd = f(d1)

        if fc <= fd:
            b1 = d1
        else:
            a1 = c1

    return (b1 + a1) / 2


start = [10, 113, 13]  # начальная точка
eps = 0.5


def gradient(start, eps):
    n = len(start)

    x0 = np.array(start)
    x_next = np.array(start)

    data = []  # данные для таблицы

    iter = 0
    while True:
        iter += 1

        # минимизация i координаты
        for i in range(n):
            x_next[i] = Diho(lambda x: f0(*[x_next[j] if j != i else x for j in range(n)]))

        data.append([iter, x0[0], x0[1], x0[2], x_next[0], x_next[1], x_next[2], f0(x0[0], x0[1], x0[2]),
                     f0(x_next[0], x_next[1], x_next[2]), norm(x0)])

        if norm(x0 - x_next) < eps:
            break

        x0 = np.copy(x_next)

    return x0, data


ans, data = gradient(start, eps)

header = ['Итерация', 'x', 'y', 'z', 'x_next', 'y_next', 'z_next', 'f(x)', 'f(x_next)', 'norm(x)']

print(tabulate(data, headers=header, tablefmt='grid', stralign='left', numalign='left'))

