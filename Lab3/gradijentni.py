from matrix import Matrix
from zlatni import *
import numpy as np

def gradijentni_spust(x0, f, df, e = 1e-6, optimalan = False):
    x = np.array(x0)
    min = None
    brojac = 0

    while(True):
        if brojac >= 100:
            #print("Postupak gradijentnog spusta divergira.")
            break
        gradijent = np.array(df(x))

        if np.linalg.norm(gradijent) < e:
            break
        v = -gradijent
        l = 1.

        if optimalan:

            v = v / np.linalg.norm(v)
            l = vrati_min(x[0], 1, lambda l: f(x + l * v))
        x += l * v
        fx = f(x)

        if min == None:
            min = fx

        elif fx < min:
            min = fx
            brojac = 0

        else:
            brojac += 1
    return x

def newton_raphson(x0, f, df, hesse_f, e = 1e-6, optimalan = False):
    x = np.array(x0)
    min = None
    brojac = 0

    while True:
        if brojac >= 100:
            #print("Newton-Raphsonov postupak diveriga.")
            break
        gradijent = np.array(df(x))
        hesse_i = np.array(Matrix(len(x0), len(x0), hesse_f(x)).inverse().data)
        v = -np.dot(hesse_i, gradijent)
        l = 1.
        if optimalan:
            v /= np.linalg.norm(v)
            l = vrati_min(x[0], 1, lambda l: f(x + l * v))
        if np.linalg.norm(l * v) < e:
            break

        x += l * v

        fx = f(x)
        if min is None:
            min = fx

        elif fx < min:
            min = fx
            brojac = 0

        else:
            brojac += 1

    return x
