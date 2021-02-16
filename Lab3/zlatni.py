from math import sqrt
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