import math

import numpy as np

def euler(A, B, x0, period, tmax, r, print_every=100):
    xs = []
    time = []
    xs.append(x0)
    t = 0
    x = x0
    i = 0
    M = np.eye(np.size(A, 1)) + A * period
    N = period * B

    while t < tmax:
        time.append(t)
        x = np.add(np.matmul(M, x), np.matmul(N, r(t)))
        xs.append(x)
        t += period
        i += 1
        if print_every != 0 and i % print_every == 0:
            print("t: {:.2f} x: {}".format(t, x.transpose()))

    return xs, time


def obrnuti_euler(A, B, x0, period, tmax, r, print_every=100):
    xs = []
    time = []
    xs.append(x0)
    t = 0
    x = x0
    i = 0
    # M = np.eye(np.size(A, 1)) + A * period
    # N = period * B
    # x = np.add(np.matmul(M, x), np.matmul(N, r(t)))
    U = np.eye(np.size(A, 1))
    P = np.linalg.inv(U - period * A)
    Q = np.matmul(P * period, B)

    while t < tmax:
        time.append(t)
        x = np.add(np.matmul(P, x), np.matmul(Q, r(t + period)))
        xs.append(x)
        t += period
        i += 1
        if print_every != 0 and i % print_every == 0:
            print("t: {:.2f} x: {}".format(t, x.transpose()))

    return xs, time


def trapez(A, B, x0, period, tmax, r, print_every=100):
    xs = []
    time = []
    xs.append(x0)
    t = 0
    x = x0
    i = 0
    U = np.eye(np.size(A, 1))
    P = U - period / 2.0 * A
    R = np.matmul(np.linalg.inv(P), U + period / 2.0 * A)
    S = np.matmul(np.linalg.inv(P), B * period / 2.0)

    while t < tmax:
        time.append(t)

        # M = np.eye(np.size(A, 1)) + A * period
        # N = period * B
        # x = np.add(np.matmul(M, x), np.matmul(N, r(t)))
        x = np.add(np.matmul(R, x), np.matmul(S, r(t) + r(t + period)))
        xs.append(x)
        t += period
        i += 1
        if print_every != 0 and i % print_every == 0:
            print("t: {:.2f}  x: {}".format(t, x.transpose()))

    return xs, time


def runge_kutta(A, B, x0, period, tmax, r, print_every=100):
    xs = []
    time = []
    xs.append(x0)
    t = 0
    x = x0
    i = 0

    while t < tmax:
        time.append(t)

        # M = np.eye(np.size(A, 1)) + A * period
        # N = period * B
        # x = np.add(np.matmul(M, x), np.matmul(N, r(t)))
        m1 = np.matmul(A, x) + np.matmul(B, r(t))
        m2 = np.matmul(A, x + m1 * period / 2.0) + np.matmul(B, r(t + period / 2.0))
        m3 = np.matmul(A, x + m2 * period / 2.0) + np.matmul(B, r(t + period / 2.0))
        m4 = np.matmul(A, x + m3 * period) + np.matmul(B, r(t + period))
        x = x + period / 6.0 * (m1 + 2 * m2 + 2 * m3 + m4)
        xs.append(x)
        t += period
        i += 1
        if print_every != 0 and i % print_every == 0:
            print("t: {:.2f}  x: {}".format(t, x.transpose()))

    return xs, time


def pece(A, B, x0, period, tmax, r, prediktor="euler", korektor="trapez", s=1, print_every=100):
    if prediktor == "euler":
        xp, tp = euler(A, B, x0, period, tmax, r, print_every=print_every)
    else:
        xp, tp = runge_kutta(A, B, x0, period, tmax, r, print_every=print_every)

    for i in range(s):
        if korektor == "obrnuti":
            xp_n, tp = obrnuti_euler(A, B, xp[0], period, tmax, r, print_every=print_every)
            xp = xp_n
        elif korektor == "trapez":
            xp_n, tp = trapez(A, B, xp[0], period, tmax, r, print_every=print_every)
            xp = xp_n

    return xp_n, tp


def pogreska(xs, ts):
    error = 0
    x_0 = xs[0][0][0]
    x_1 = xs[1][0][0]
    for i in range(len(ts)):
        t = ts[i]
        x1 = xs[i][0][0]
        x2 = xs[i][1][0]
        x1_ = x_0 * math.cos(t) + x_1 * math.sin(t)
        x2_ = x_1 * math.cos(t) - x_0 * math.sin(t)
        error += abs(x1_ - x1) + abs(x2_ - x2)
    return error


def r1(t):
    # return np.array(0, n)
    return np.array([[0], [0]])


# A = np.array([[0, 1], [-1, 0]])
# B = np.array([[0, 0], [0, 0]])

# xs, ts = euler(A, B, np.array([[1], [1]]), 0.01, 10, r1)
# xs, ts = obrnuti_euler(A, B, np.array([[1], [1]]), 0.01, 10, r1)
# xs, ts = runge_kutta(A, B, np.array([[1], [1]]), 0.01, 10, r1)
# xp, tp = pece(A, B, np.array([[1], [1]]), 0.01, 10, r1, print_every=0)
