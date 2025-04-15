import numpy as np
import scipy.optimize as opt

def f0(x):
    return np.exp(-0.01 * 12 * x) + np.exp(0.01 * x) + x**2

# определим функцию
def f(x):
    return np.exp(-0.01 * 12 * x) + np.exp(0.01 * x) + x**2

# начальные параметры
start = -100
end = 100
e0 = 1e-5
v = 1e-6

# метод дихотомии
def Diho(a, b):

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


# взятое готовое решение из scipy.optimize
result = opt.minimize_scalar(f0, bounds=(start, end), method='bounded')

ans = Diho(start, end)

print("Приблизительное и точное решение: ",ans, result.x)



