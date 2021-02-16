import random
from math import sqrt, sin
import numpy as np
#Postupak trazenja unimodalnog intervala

# Ulazne velicine:
# - tocka: pocetna tocka pretrazivanja
# - h: pomak pretrazivanja
# - f: ciljna funkcija
#
# Izlazne vrijednosti:
# - unimodalni interval [l, r]

def unimodalni(tocka, h, f):
    l = tocka - h
    r = tocka + h
    m = tocka
    step = 1
    fm = f(tocka)
    fl = f(l)
    fr = f(r)

    if fm < fr and fm < fl:
        return l, r

    if fm > fr:
        while True:
            l = m
            m = r
            step *= 2
            r = tocka + h * step
            fr = f(r)
            if not fm > fr:
                break

    else:
        while True:
            r = m
            m = l
            step *= 2
            l = tocka - h * step
            fl = f(l)
            if not fm > fl:
                break

    return l, r

# Algoritam zlatnog reza
#
# ulazne velicine:
# - a, b: pocetne granice unimodalnog intervala
# - e: preciznost

def zlatni_rez(a, b, f, e = 1e-6):
    k = 0.5 * (sqrt(5) - 1)
    c = b - k * (b - a)
    d = a + k * (b - a)
    fc = f(c)
    fd = f(d)

    while (b - a) > e:
        if fc < fd:
            b = d
            d = c
            c = b - k * (b - a)
            fd = fc
            fc = f(c)
        else:
            a = c
            c = d
            d = a + k * (b - a)
            fc = fd
            fd = f(d)

    return a, b

def vrati_min(tocka, h, f):
    [l, r] = unimodalni(tocka, h, f)
    [l, r] = zlatni_rez(l, r, f)
    return (l + r) / 2

def pretrazivanje_po_koord_osima(x0, f, e = 1e-6):
    x = np.array(x0)
    ei = np.array([0] * len(x0))

    while True:
        xs = x.copy()
        for i in range(len(x0)):
            ei[i] = 1
            fja = lambda l : f(x + l * ei)
            l_min = vrati_min(xs[i], 1, fja)
            x = x + l_min * ei
            ei[i] = 0
        if all(abs(x - xs) <= e):
            break

    return x

def odredi_indekse(x, f, e = 1e-6):
    max = min = f(x[0])
    h = l = 0
    for i in range(len(x)):
        xi = x[i]
        fi = f(xi, j=0)
        if fi - max > e:
            max = f(xi, j=0)
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

        if f(xr,j=0) < f(simplex[l],j=0):
            xe = ekspanzija(xc, xr, gamma)
            if f(xe,j=0) < f(simplex[l],j=0):
                simplex[h] = xe
            else:
                simplex[h] = xr
        else:
            uvjet = True
            for i in range(len(simplex)):
                if i == h:
                    continue
                if f(xr,j=0) <= f(simplex[i],j=0):
                    uvjet = False
                    break

            if uvjet:
                if f(xr,j=0) < f(simplex[h],j=0):
                    simplex[h] = xr

                xk = kontrakcija(xc, simplex[h], beta)

                if f(xk,j=0) < f(simplex[h], j = 0):
                    simplex[h] = xk
                else:
                    # POMAKNI SVE TOČKE
                    #xs = simplex, mov = simplex[l, sigma = sigma
                    simplex = pomakni_tocke(simplex, simplex[l], sigma)
            else:
                simplex[h] = xr

            zbroj = 0
            for i in range(len(simplex)):
                zbroj += (f(simplex[i], j = 0) - f(xc)) ** 2

            if sqrt(float(zbroj) / len(simplex)) <= e:
                return xc


def istrazi(xp, dx, f):
    x = np.array(xp)
    for i in range(len(x)):
        p = float(f(x))
        x[i] = x[i] + dx
        n = float(f(x))

        if n > p:
            x[i] = x[i] - 2 * dx
            n = float(f(x))
            if n > p:
                x[i] = x[i] + dx
    return x

def hooke_jeeves(x0, f, dx = 0.5, e = 1e-6):
    xp = xb = x0
    while True:
        xn = istrazi(xp, dx, f)
        if f(xn) < f(xb):
            xp = 2 * xn - xb
            xb = xn
        else:
            dx = dx / 2.
            xp = xb
        #print(xb, xp, xn)
        if dx < e:
            return xb


def f1(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2

def f2(x):
    return (x[0] - 4) ** 2 + 4 * (x[1] - 2) ** 2

def f3(x):
    sum = 0
    for xi, i in enumerate(x):
        sum += (xi - i) ** 2
    return sum

def f4(x):
    return abs((x[0] - x[1]) * (x[0] + x[1])) + sqrt(x[0] ** 2 + x[1] ** 2)

def f6(x):
    sum = 0
    for xi in x:
        sum += xi ** 2
    zbroj = sqrt(sum)
    return 0.5 + (sin(zbroj) ** 2 - 0.5) / ((1 + 0.001 * zbroj) ** 2)

def prva(x):
    return (x - 3) ** 2


# PRVI ZADATAK
print("\nPRVI ZADATAK")
brojac = [-1]
ys = dict()
def f(x, c = brojac, y = ys, j=1):
    c[0] += j
    if not y.get(str(x)):
        y[str(x)] = prva(x)
    return y[str(x)]

for i in range(10, 200, 20):
    x0 = np.array([float(i)])
    print("Početna točka je ", x0)

    y = vrati_min(x0, 1, f)
    print("\tZlatni rez : ", y, " u ", brojac[0], " iteracija.")
    brojac[0] = -1
    f(0, brojac)

    y = pretrazivanje_po_koord_osima(x0, f)
    print("\tPo koordinatnim osima : ", y, " u ", brojac[0], " iteracija.")
    brojac[0] = -1
    f(0, brojac)

    y = hooke_jeeves(x0, f)
    print("\tHooke - Jeeves : ", y, " u ", brojac[0], " iteracija.")
    brojac[0] = -1
    f(0, brojac)

print("-" * 150, "\n")
# DRUGI ZADATAK
print("DRUGI ZADATAK")
funkcije = [f2, f3, f4]
pocetne_tocke = [np.array([-1.9, 2]), np.array([0.1, 0.3]), np.array([0.0, 0, 0, 0, 0]), np.array([5.1, 1.1])]
for i in range(len(funkcije)):
    print("Funkcija f", i + 1)
    brojac = [-1]
    ys = dict()
    def f(x, c=brojac, y=ys, j = 1):
        c[0] += j
        if not y.get(str(x)):
            y[str(x)] = funkcije[i](x)
        return y[str(x)]

    xc = simpleks(pocetne_tocke[i], f)
    print("\tSimpleks po Nelderu i Meadu:", xc, "u ", brojac[0], "iteracija.")
    brojac[0] = -1
    f(pocetne_tocke[i], brojac)

    xm = pretrazivanje_po_koord_osima(pocetne_tocke[i], f)
    print("\tPo koordinatnim osima : ", xm, " u ", brojac[0], " iteracija.")
    brojac[0] = -1
    f(pocetne_tocke[i], brojac)

    xb = hooke_jeeves(pocetne_tocke[i], f)
    print("\tHooke-Jeeves:", xb, "u", brojac[0], "iteracija.")
    brojac[0] = -1
    f(pocetne_tocke[i], brojac)

print("-" * 150, "\n")
# TRECI ZADATAK
print("TRECI ZADATAK")
x0 = np.array([5.0, 5.0])
brojac = [-1]
ys = dict()
def f(x, c=brojac, y=ys, j=1):
    c[0] += j
    if not y.get(str(x)):
        y[str(x)] = f4(x)
    return y[str(x)]


xc = simpleks(x0, f)
print("\tSimpleks po Nelderu i Meadu:", xc, "u ", brojac[0], "iteracija.")
brojac[0] = -1
f(x0, brojac)

xb = hooke_jeeves(x0, f)
print("\tHooke-Jeeves:", xb, "u", brojac[0], "iteracija.")
brojac[0] = -1
f(x0, brojac)

print("-" * 150, "\n")
# CETVRTI ZADATAK
print("CETVRTI ZADATAK")
brojac = [-1]
ys = dict()
def f(x, c=brojac, y=ys, j=1):
    c[0] += j
    if not y.get(str(x)):
        y[str(x)] = f1(x)
    return y[str(x)]
x0 = np.array([0.5, 0.5])
print("Početna točka [0.5, 0.5]")
for korak in range(20):
    print("Korak za generiranje=", korak + 1)
    xc = simpleks(x0, f, korak + 1)
    print("\tMinimum:", xc, "u ", brojac[0], "iteracija.")
    brojac[0] = -1
    f(x0, brojac)

x0 = np.array([20.0, 20.0])
print("Početna točka [20, 20]")
for korak in range(20):
    print("Korak za generiranje=", korak + 1)
    xc = simpleks(x0, f, korak + 1)
    print("\tMinimum:", xc, "u ", brojac[0], "iteracija.")
    brojac[0] = -1
    f(x0, brojac)

print("-" * 100, "\n")
# PETI ZADATAK
print("PETI ZADATAK")
pronadeno = 0

brojac = [-1]
ys = dict()
def f(x, c=brojac, y=ys, j=1):
    c[0] += j
    if not y.get(str(x)):
        y[str(x)] = f6(x)
    return y[str(x)]

for i in range(100):
    x = random.randrange(-50, 51)
    y = random.randrange(-50, 51)
    x0 = np.array([x, y])

    xc = simpleks(x0, f)
    if f(xc) < 1e-4:
        pronadeno += 1

print("Vjerojatnost pronadenih:", float(pronadeno)/100)