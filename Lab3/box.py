import random
import numpy as np

from simpleks import centroid


def box(x0, f, xd, xg, g, e = 1e-6, alfa = 1.3):
    n = len(x0)
    for i in range(len(g)):
        if not g[i](x0) >= 0:

            print("Početna točka ne zadovoljava implicitna ograničenja.")
            return None

    for i in range(n):
        if not xd[i] <= x0[i] <= xg[i]:

            print("Početna točka ne zadovoljava eksplicitna ograničenja.")
            return None

    #2n točaka
    x = np.empty([2 * n, n])

    xc = np.array([x0])

    for i in range(2 * n):
        for j in range(n):

            x[i, j] = xd[j] + random.random() * (xg[j] - xd[j])
            #print(x[i, j])

        brojac = 0
        for j in range(len(g)):
            while g[j](x[i]) < 0:

                brojac += 1
                if brojac >= 100:
                    #print("Postupak po Boxu divergira.")
                    break
                x[i] = (x[i] + xc) / 2.

           # xc = np.array([0] * n)
            xc = np.empty(n)

            for j in range(i):
                xc += x[j]

            xc /= i + 2
        broj = 0
        min = None
        fx = np.array([f(x[i]) for i in range(2 * n)])
        while True:

            if broj >= 100:
                #print("Postupak po Boxu divergira.")

                break
            l = np.argmin(fx); h = np.argmax(fx)

            zast = True

            for i in range(2 * n):
                if zast and i != h:

                    h2 = i
                    zast = False

                elif i != h and fx[h2] < fx[i]:
                    h2 = i

            xc = np.empty(n)

            # xc = centroid(np.array(x), h)
            # print(xc)

            for i in range(2 * n):
                if i != h:
                    xc += x[i]

            xc /= 2 * n

            #print(xc)

            xr = (1 + alfa) * xc - alfa * x[h]

            for i in range(n):

                if xr[i] > xg[i]:
                    xr[i] = xg[i]

                elif xr[i] < xd[i]:
                    xr[i] = xd[i]

            brojac = 0

            for i in range(len(g)):
                while g[i](xr) < 0:
                    brojac += 1
                    if brojac >= 100:
                        # print("Postupak po Boxu divergira.")
                        break
                    xr = (xr + xc) / 2.

            fxr = f(xr)

            if fxr > fx[h2]:
                xr = (xr + xc) / 2.
                fxr = f(xr)

            x[h] = xr
            fx[h] = fxr

            for i in range(n):
                if abs(x[h][i] - xc[i]) < e:
                    break
            fxc = f(xc)

            if min is None:
                min = fxc

            elif fxc < min:
                min = fxc
                broj = 0

            else:
                broj += 1

    return x[l]
