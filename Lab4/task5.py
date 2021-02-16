from functions import *

from genetic_algorithm import GeneticAlgorithm

n = 40
chromosome = "float"
lower_limit = -50
upper_limit = 150
dimension = 3
crossover_fn = "arithmetic" # UNIFORM
b = 5
precision = 4
pm = 0.3
aas = [1, 2]

for a in aas:
    g1 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, a)
    g1.run(f6, steps=10000, print_every=1000)

