from lab import *
import matplotlib.pyplot as plt

A = np.array([[1, -5], [1, -7]])
B = np.array([[5, 0], [0, 3]])


def r1(t):
    return np.array([[t], [t]])


x0 = np.array([[-1], [3]])


print("EULEROV POSTUPAK")
xs, ts = euler(A, B, x0, 0.01, 1, r1, print_every=10)

values1 = []
values2 = []
for i in range(len(ts)):
    values1.append(xs[i][0][0])
    values2.append(xs[i][1][0])

plt.suptitle("Euler")
plt.plot(ts, values1, label="x1")
plt.plot(ts, values2, label="x2")
plt.legend(loc='best')
plt.grid()
plt.show()


print("OBRNUTI EULEROV POSTUPAK")
xs, ts = obrnuti_euler(A, B, x0, 0.01, 1, r1, print_every=10)

values1 = []
values2 = []
for i in range(len(ts)):
    values1.append(xs[i][0][0])
    values2.append(xs[i][1][0])

plt.suptitle("Obrnuti Euler")
plt.plot(ts, values1, label="x1")
plt.plot(ts, values2, label="x2")
plt.legend(loc='best')
plt.grid()
plt.show()


print("TRAPEZNI POSTUPAK")
xs, ts = trapez(A, B, x0, 0.01, 1, r1, print_every=10)

values1 = []
values2 = []
for i in range(len(ts)):
    values1.append(xs[i][0][0])
    values2.append(xs[i][1][0])

plt.suptitle("Trapezni")
plt.plot(ts, values1, label="x1")
plt.plot(ts, values2, label="x2")
plt.legend(loc='best')
plt.grid()
plt.show()


print("RUNGE-KUTTA POSTUPAK 4. REDA")
xs, ts = runge_kutta(A, B, x0, 0.01, 1, r1, print_every=10)

values1 = []
values2 = []
for i in range(len(ts)):
    values1.append(xs[i][0][0])
    values2.append(xs[i][1][0])

plt.suptitle("Runge-Kutta")
plt.plot(ts, values1, label="x1")
plt.plot(ts, values2, label="x2")
plt.legend(loc='best')
plt.grid()
plt.show()


print("PREDIKTORSKO-KOREKTORSKI POSTUPAK")
xs, ts = pece(A, B, x0, 0.01, 1, r1, print_every=0)
for x, t in list(zip(xs, ts))[::10]:
    print("t: {:.2f}  y:[{}, {}]".format(t, x[0][0], x[1][0]))
values1 = []
values2 = []
for i in range(len(ts)):
    values1.append(xs[i][0][0])
    values2.append(xs[i][1][0])

plt.suptitle("Prediktorsko-korektorski")
plt.plot(ts, values1, label="x1")
plt.plot(ts, values2, label="x2")
plt.legend(loc='best')
plt.grid()
plt.show()