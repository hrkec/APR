import numpy as np
from math import sqrt

def odredi_indekse(x, f, e = 1e-6):
    max = min = f(x[0])
    h = l = 0
    for i in range(len(x)):
        xi = x[i]
        fi = f(xi)
        if fi - max > e:
            max = f(xi)
            h = i
        if min - fi > e:
            min = fi
            l = i
    return h, l

def centroid(x, h):
    #xc = np.zeros(len(x[0]))
    xc = [0] * len(x[0])
    for i in range(len(x)):
        if i == h:
            continue
        for j in range(len(x[i])):
            xc[j] += x[i][j]
    n = len(xc)
    for i in range(n):
        xc[i] /= float(n)
    return xc

def refleksija(xc, xh, alpha):
    xc = np.array(xc)
    xh = np.array(xh)
    xr = (1 + alpha) * xc - alpha * xh
    return xr

def ekspanzija(xc, xr, gamma):
    xc = np.array(xc)
    xr = np.array(xr)
    xe = (1 - gamma) * xc + gamma * xr
    return xe

def kontrakcija(xc, xh, beta):
    xc = np.array(xc)
    xh = np.array(xh)
    xk = (1 - beta) * xc + beta + xh
    return xk


def pomakni_tocke(xs, mov, sigma):
    xs2 = []
    move = np.array(mov)
    for x in xs:
        rez = sigma * (np.array(x) + move)
        xs2.append(rez.tolist())

    return xs2

def simpleks(x0, f, move = 1, alpha = 1, beta = 0.5, gamma = 2, sigma = 0.5, e = 1e-6):
    simplex = [x0]

    for i in range(len(x0)):
        x = np.array(x0)
        x[i] = x0[i] + move
        simplex.append(x)

    cnt = 0
    while True:
        h, l = odredi_indekse(simplex, f)
        # print("SIMPLEX = ", simplex)
        # print("H, L = ", h , l)
        xc = centroid(simplex, h)
        # print("Centroid = ", xc)
        xr = refleksija(xc, simplex[h], alpha)
        # print(" XR = ", xr)

        if cnt > 10000:
            return xc
        else:
            cnt += 1

        if f(xr) < f(simplex[l]):
            xe = ekspanzija(xc, xr, gamma)
            if f(xe) < f(simplex[l]):
                simplex[h] = xe
            else:
                simplex[h] = xr
        else:
            uvjet = True
            for i in range(len(simplex)):
                if i == h:
                    continue
                if f(xr) <= f(simplex[i]):
                    uvjet = False
                    break

            if uvjet:
                if f(xr) < f(simplex[h]):
                    simplex[h] = xr

                xk = kontrakcija(xc, simplex[h], beta)

                if f(xk) < f(simplex[h]):
                    simplex[h] = xk
                else:
                    # POMAKNI SVE TOČKE
                    #xs = simplex, mov = simplex[l, sigma = sigma
                    simplex = pomakni_tocke(simplex, simplex[l], sigma)
            else:
                simplex[h] = xr

            zbroj = 0
            for i in range(len(simplex)):
                zbroj += (f(simplex[i]) - f(xc)) ** 2

            if sqrt(float(zbroj) / len(simplex)) <= e:
                return xc