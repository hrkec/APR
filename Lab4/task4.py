from functions import *

from genetic_algorithm import GeneticAlgorithm

ns = [30, 50, 100, 200]
# ns = [50, 100, 200]
chromosome = "float"
lower_limit = -50
upper_limit = 150
dimension = 3
crossover_fn = "arithmetic" # UNIFORM
b = 5
precision = 4
pms = [0.1, 0.3, 0.6, 0.9]
a = 1

for n in ns:
    for pm in pms:
        print("Optimizacija funkcije f6, populacija", n, " pm", pm)
        count = 0
        for i in range(10):
            g = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
            g.run(f6, steps=1000, print_every=0)
            if(g.best_value() < 10e-6):
                count += 1
            print( g.best_value())
        print("Broj pronadenih minimuma:", count, "/10")
        count = 0
