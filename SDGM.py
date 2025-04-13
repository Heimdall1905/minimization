from tabulate import tabulate
import numpy as np

my_g = 0
my_norm = 0
# наша функция, для которой мы ищем минимум
def f0(x, y, z):
    global my_g
    my_g += 1
    return 5 * (x - 12) ** 2 + 5 * (y - 1) ** 2 + 5 * (z - 1) ** 2 + 2 * (x - 12) * (y - 1) + 2 * (x - 12) * (z - 1) + 2 * (y - 1) * (z - 1)

# частные производные нашей функции
def X(m):
    return 10 * (m[0] - 12) + 2 * (m[1] - 1) + 2 * (m[2] - 1)

def Y(m):
    return 10 * (m[1] - 1) + 2 * (m[0] - 12) + 2 * (m[2] - 1)


def Z(m):
    return 10 * (m[2] - 1) + 2 * (m[0] - 12) + 2 * (m[1] - 1)

# градиент вектора
def grad(m):
    return np.array([X(m), Y(m), Z(m)])

# норма вектора
def norm(m):
    global my_norm
    my_norm += 1
    return np.sqrt(X(m) ** 2 + Y(m) ** 2 + Z(m) ** 2)

# метод дихотомии
def Diho(x0):
    a = -100
    b = 100
    e0 = 1e-5
    v = 1e-6

    f = lambda a: f0(x0[0] - a * X(x0), x0[1] - a * Y(x0), x0[2] - a * Z(x0))
    # можно было по умнее, конечно, как f0(*<разность массивов какая-нибудь>)

    a1 = a
    b1 = b

    while (b1 - a1)  > e0 :

        c1 = (a1 + b1) / 2 - v / 2
        fc = f(c1)
        d1 = (a1 + b1) / 2 + v / 2
        fd = f(d1)

        if fc <= fd:
            b1 = d1
        else:
            a1 = c1

    return (b1 + a1) / 2

# направленный спуск
def triad(x0, eps, iter):
  data_triad = []
  a = 0
  step = 1.1
  f = lambda a: f0(x0[0] - a * X(x0), x0[1] - a * Y(x0), x0[2] - a * Z(x0))


  flag = False
  flah = False
  x_last = a
  f_last = f(x_last)
  while True:
    x_next = x_last
    x_next = x_next + step

    if x_next <= 0:
      step /= 2
      step *= -1
      continue


    f_next = f(x_next)

    data_triad.append([x_last, x_next, f_last, f_next, step])

    if f_next < f_last:
      flag = False
      flah = True
      x_last = x_next
      f_last = f_next

    else:
      if f_next > f_last and flag == False:
        flag = True
        step *= -1
      else:
        flag = False
        step /= 2
        if abs(step) < eps:
          a = x_last
          break
  return a, data_triad



start = [51, 12, 62] # начальная точка
eps = 0.05

def gradient(start, eps):
    global my_g
    global my_norm
    header_triad = ["x0", "x1", "f(x0)", "f(x1)", "step"]
    x0 = start
    data = [] # данные для таблицы
    iter = 0
    while norm(x0) > eps:
        iter += 1

        a, data_triad = triad(x0, 10 ** (-iter), iter) # находим коэффициент альфа
        x_next = x0 - a * grad(x0) # сдвигаем вектор в сторону антиградиента
        print(f"Шаг {iter}")
        print(tabulate(data_triad, headers=header_triad, tablefmt='grid', stralign='left', numalign='left'))

        data.append([iter, x0[0], x0[1], x0[2], x_next[0], x_next[1], x_next[2], f0(x0[0], x0[1], x0[2]), f0(x_next[0], x_next[1], x_next[2]), norm(x0), a, my_g, my_norm, grad(x0)])

        x0 = x_next # обновляем вектор

    return x0, data

ans, data = gradient(start, eps)

header = ['Шаг', 'x', 'y', 'z', 'x_next', 'y_next', 'z_next', 'f(x)', 'f(x_next)', 'norm(x)', 'a', 'Вызов функции', 'Вызов нормы', 'Градиент']

print("Точка минимума - ", ans)
print(tabulate(data, headers=header, tablefmt='grid', stralign='left', numalign='left'))
