import numpy as np

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
