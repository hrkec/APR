from functions import *

from genetic_algorithm import GeneticAlgorithm

n = 40
chromosome = "float"
lower_limit = -50
upper_limit = 150
dimensions = [1, 3, 6, 10]
crossover_fn = "arithmetic" # UNIFORM
b = 5
precision = 4
pm = 0.3
a = 1

functions = [f6, f7]

for i, f in enumerate(functions):
    for dimension in dimensions:
        print("Optimizacija funkcije", i + 6, ", dimenzionalnosti", dimension)
        g = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
        g.run(f, steps = 10000, print_every=500)
