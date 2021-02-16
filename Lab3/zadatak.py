import numpy as np
import gradijentni
import hj
from box import box

class Funkcija:
    def __init__(self, f):
        self.f = f
        self.broj = 0
        self.ys = dict()

    def izracunaj(self, x):
        self.broj += 1
        if not self.ys.get(str(x)):
            self.ys[str(x)] = self.f(x)
        return self.ys[str(x)]

    def reset(self):
        self.broj = 0

def f1(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2

def gf1(x):
    gradijent = []
    gradijent.append(-400 * x[0] * (x[1] - x[0] ** 2) - 2 * (1 - x[0]))
    gradijent.append(200 * (x[1] - x[0] ** 2))
    return gradijent

def hf1(x):
    hesse = []
    hesse.append([1200 * x[0] ** 2 - 400 * x[1] + 2, -400 * x[0]])
    hesse.append([-400 * x[0], 200])
    return hesse

def f1g1(x):
    return x[1] - x[0]

def f1g2(x):
    return 2 - x[0]

def f2(x):
    return (x[0] - 4) ** 2 + 4 * (x[1] - 2) ** 2

def gf2(x):
    gradijent = []
    gradijent.append(2 * x[0] - 8)
    gradijent.append(8 * x[1] - 16)
    return gradijent

def hf2(x):
    hesse = []
    hesse.append([2, 0])
    hesse.append([0, 8])
    return hesse

def f3(x):
    return (x[0] - 2) ** 2 + (x[1] + 3) ** 2

def gf3(x):
    gradijent = []
    gradijent.append(2 * x[0] - 4)
    gradijent.append(2 * x[1] + 6)
    return gradijent

def hf3(x):
    return [[2, 0], [0, 2]]

def f4(x):
    return (x[0] - 3) ** 2 + (x[1]) ** 2

def gf4(x):
    return [2 * x[0] - 6, 2 * x[1]]

def hf4(x):
    return [[2, 0], [0, 2]]

def f4g1(x):
    return 3 - x[0] - x[1]

def f4g2(x):
    return 3 + 1.5 * x[0] - x[1]

def f4h1(x):
    return x[1] - 1


#PRVI ZADATAK
print("PRVI ZADATAK")
x0 = np.array([0.0, 0])
f = Funkcija(f3)
gf = Funkcija(gf3)
xmin = gradijentni.gradijentni_spust(x0, f.izracunaj, gf.izracunaj)
print("\tBez određivanja optimalnog iznosa:", xmin, f3(xmin), f.broj, gf.broj)

f.reset(); gf.reset()

xmin = gradijentni.gradijentni_spust(x0, f.izracunaj, gf.izracunaj, optimalan=True)
print("\tS određivanjem optimalnog iznosa:", xmin, f3(xmin), f.broj, gf.broj)

print("-" * 150)
#DRUGI ZADATAK
print("DRUGI ZADATAK")
x0 = np.array([-1.9, 2])
f = Funkcija(f1)
gf = Funkcija(gf1)
hf = Funkcija(hf1)
xmin = gradijentni.gradijentni_spust(x0, f.izracunaj, gf.izracunaj, optimalan=True)
print("f1:")
print("\tGradijentni spust: ", xmin, f1(xmin), f.broj, gf.broj)
f.reset(); gf.reset()
xmin = gradijentni.newton_raphson(x0, f.izracunaj, gf.izracunaj, hf.izracunaj, optimalan=True)
print("\tNewton-Raphsonov: ", xmin, f1(xmin), f.broj, gf.broj, hf.broj)

x0 = np.array([0.1, 0.3])
f = Funkcija(f2)
gf = Funkcija(gf2)
hf = Funkcija(hf2)
xmin = gradijentni.gradijentni_spust(x0, f.izracunaj, gf.izracunaj, optimalan=True)
print("f2:")
print("\tGradijentni spust: ", xmin, f2(xmin), f.broj, gf.broj)
f.reset(); gf.reset()
xmin = gradijentni.newton_raphson(x0, f.izracunaj, gf.izracunaj, hf.izracunaj, optimalan=True)
print("\tNewton-Raphsonov: ", xmin, f2(xmin), f.broj, gf.broj, hf.broj)

print("-" * 150)
#TRECI ZADATAK
print("TRECI ZADATAK")

x0 = np.array([-1.9, 2])
f = Funkcija(f1)
xmin = box(x0, f.izracunaj, [-100, -100], [100, 100], [f1g1, f1g2])
print("f1:")
print("\tPo Boxu:", xmin, f1(xmin))

x0 = np.array([0.1, 0.3])
f = Funkcija(f2)
xmin = box(x0, f.izracunaj, [-100, -100], [100, 100], [f1g1, f1g2])
print("f2:")
print("\tPo Boxu:", xmin, f2(xmin))

print("-" * 150)
#CETVRTI ZADATAK
print("CETVRTI ZADATAK")
