from math import sqrt
from math import sin


def f1(x):
    return 100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2


def f3(x):
    sum = 0
    for i, e in enumerate(x):
        sum += (e - i - 1)**2
    return sum


def f6(x):
    sum = 0
    for e in x:
        sum += e ** 2
    b = (sin(sqrt(sum))) ** 2 - 0.5
    n = (1 + 0.001 * sum) ** 2
    return 0.5 + b / n


def f7(x):
    sum = 0
    for e in x:
        sum += e ** 2
    p = sum ** 0.25
    d = 1 + sin(50 * sum ** 0.1) ** 2
    return p * d
