import numpy as np
import scipy.optimize as opt
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
h0 = 1
x_start = 0

# метод направленного спуска
def Foo(a, b, h, start_x):
    trr = [0, 0]
    data = []
    data1 = []
    x0 = start_x
    y0 = f(x0, trr)

    iter = 0
    # этап 0
    x1 = x0 + h
    y1 = f(x1, trr)

    x2 = x0 - h
    y2 = f(x2, trr)

    flag = True

    if y1 < y0:
        x_left = x0
        y_left = y0
        x0 = x1
        y0 = y1
        x_right = x0 + h
        y_right = f(x_right, trr)
    elif y2 < y0:
        x_right = x0
        y_right = y0
        x0 = x2
        y0 = y2
        x_left = x0 - h
        y_left = f(x_left, trr)
    else:
        flag = False
    data1.append({
        'Итерация': iter,
        'Глобальная трудоемкость': trr[1],
        'Шаг': round(h, 8),
        # 'x0': x2,
        'f(x0)': round(y2, 4),
        # 'x1': x0,
        'f(x1)': round(y0, 4),

        # 'x2': x1,
        'f(x2)': round(y1, 4),
    })

    # этап 1
    if flag:
        while True:
            trr[0] = 0
            iter += 1
            x1 = x_right
            y1 = y_right

            x2 = x_left
            y2 = y_left
            if y1 < y0:
                x_left = x0
                y_left = y0
                x0 = x1
                y0 = y1
                x_right = x0 + h
                y_right = f(x_right, trr)
            elif y2 < y0:
                x_right = x0
                y_right = y0
                x0 = x2
                y0 = y2
                x_left = x0 - h
                y_left = f(x_left, trr)
            else:
                break
            data1.append({
                'Итерация': iter,
                'Глобальная трудоемкость': trr[1],
                'Шаг': round(h, 8),
                # 'x0': x2,
                'f(x0)': round(y2, 4),
                # 'x1': x0,
                'f(x1)': round(y0, 4),

                # 'x2': x1,
                'f(x2)': round(y1, 4),
            })

    # этап 2
    # наша триада: х2, х0, х1
    change = True
    iter = 0
    trr = [0, 0]
    h_iter = 0
    h /= 2
    while abs(h) > e0 / 2:
        trr[0] = 0
        iter += 1



        # делаем шаг
        x_next = x0 + h
        y_next = f(x_next, trr)

        data.append({
            'Итерация': iter,
            'Глобальная трудоемкость': trr[1],
            'Шаг': round(h, 8),
            # 'x0': x2,
            'f(x0)': round(y2, 4),
            # 'x1': x0,
            'f(x1)': round(y0, 4),

            # 'x2': x1,
            'f(x2)': round(y1, 4),
            'f(next)': round(y_next, 4),
        })

        # если меньше, то продолжаем туда идти
        if y_next < y0:
            x2 = x0
            y2 = y0
            x0 = x_next
            y0 = y_next
        # если больше, то разворачиваемся, при этом, если мы этот шаг проверили уже два раза, то
        # повторно разворачиваться не нужно, уменьшаем в два раза и проверяем в том же направлении
        elif y0 < y_next and h_iter == 0:
            h = -h
            h_iter = 1
            x1 = x2
            y1 = y2
            x2 = x_next
            y2 = y_next
        else:
            h /= 2
            h_iter = 0



    return x0, data, data1

# взятое готовое решение из scipy.optimize
result = opt.minimize_scalar(f0, bounds=(start, end), method='bounded')

# задача три
ans = Foo(start, end, h0, x_start)
print(tabulate(ans[2], headers="keys", tablefmt="pretty"))
print(tabulate(ans[1], headers="keys", tablefmt="pretty"))
print("Приблизительное и точное решение: ",round(ans[0], 6), round(result.x, 6))