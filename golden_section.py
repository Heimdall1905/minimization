import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from tabulate import tabulate

def f0(x):
    return np.exp(-0.01 * 12 * x) + np.exp(0.01 * x) + x**2

# определим функцию
def f(x, trr):
    trr[0] += 1
    trr[1] += 1
    return np.exp(-0.01 * 12 * x) + np.exp(0.01 * x) + x**2

# начальные параметры
start = -100
end = 100
e0 = 1e-5
v = 1e-6

# метод золотого сечения
def Golden(a, b):
    print("Метод золотого сечения")
    iter = 0
    trr = [0, 0]
    data = []
    xg = []
    yg = []
    a1 = a
    b1 = b
    c1 = (3 - np.sqrt(5)) * (b1 - a1) / 2 + a1
    d1 = (np.sqrt(5) - 1) * (b1 - a1) / 2 + a1
    fc = f(c1, trr)
    fd = f(d1, trr)
    # нулевая итерация, далее уже по одному разу считаем на каждой итерации
    #print(f"Итерация {iter}, локальная трудоёмкость {trr[1]}, точка c:{c1}, точка d:{d1}")
    data.append({
        'Шаг': iter,
        'Локальная трудоемкость': trr[1],
        'Глобальная трудоемкость': trr[0],
        'Погрешность': round((b1 - a1) / 2, 8),
        'Левая граница': round(a1, 8),
        'Правая граница': round(b1, 8),
    })

    xg.append(c1)
    xg.append(d1)
    yg.append(fc)
    yg.append(fd)

    while (b1 - a1) / 2 > e0 / 2:
        trr[1] = 0
        iter += 1

        if fc <= fd:
            b1 = d1
            d1 = c1
            fd = fc
            c1 = (3 - np.sqrt(5)) * (b1 - a1) / 2 + a1
            fc = f(c1, trr)
            xg.append(c1)
            yg.append(fc)

        else:
            a1 = c1
            c1 = d1
            fc = fd
            d1 = (np.sqrt(5) - 1) * (b1 - a1) / 2 + a1
            fd = f(d1, trr)
            xg.append(d1)
            yg.append(fd)

        #print(f"Итерация {iter}, локальная трудоёмкость {trr[1]}, точка c:{c1}, точка d:{d1}")
        # вывод информации на каждом шаге
        data.append({
            'Шаг': iter,
            'Локальная трудоемкость': trr[1],
            'Глобальная трудоемкость': trr[0],
            'Погрешность': round((b1 - a1) / 2, 8),
            'Левая граница': round(a1, 8),
            'Правая граница': round(b1, 8),
        })

    #print(f"Глобальная трудоёмкость {trr[0]}")
    return (b1 + a1) / 2, xg, yg, data

# взятое готовое решение из scipy.optimize
result = opt.minimize_scalar(f0, bounds=(start, end), method='bounded')

x = np.linspace(start, end, 1000)
y = f0(x)

ansg = Golden(start, end)
# Таблица информации
print(tabulate(ansg[3], headers="keys", tablefmt="pretty"))
print("Приблизительное и точное решение: ",ansg[0], result.x)

# чертим график
plt.figure(2)
plt.plot(x, y, color = 'yellow', zorder = 1) # наша функция
plt.scatter([result.x, ansg[0]], [result.fun, f0(ansg[0])], color = 'black', zorder = 3) # точное решение
plt.scatter(ansg[1], ansg[2], color = 'red', zorder = 2)
plt.show()