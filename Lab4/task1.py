from functions import *

from genetic_algorithm import GeneticAlgorithm

n = 40
chromosome = "float"
lower_limit = -50
upper_limit = 150
dimension = 2
crossover_fn = "arithmetic" # UNIFORM
b = 5
precision = 4
pm = 0.3
a = 1

print("Optimizacija funkcije f1 s pomicnom tockom")
g1 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
g1.run(f1, steps=10000, print_every=500)

chromosome = "binary"
crossover_fn = "uniform"
print("Optimizacija funkcije f1 binarni")
g1 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
g1.run(f1, steps=10000, print_every=500)


dimension = 5
chromosome = "float"
crossover_fn = "arithmetic"
print("Optimizacija funkcije f3 s pomicnom tockom")

g3 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
g3.run(f3, steps=10000, print_every=500)


chromosome = "binary"
crossover_fn = "uniform"
print("Optimizacija funkcije f3 binarni")

g3 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
g3.run(f3, steps=10000, print_every=500)



dimension = 2
chromosome = "float"
crossover_fn = "arithmetic"
print("Optimizacija funkcije f6 s pomicnom tockom")

g6 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
g6.run(f6, steps=10000, print_every=500)


chromosome = "binary"
crossover_fn = "uniform"
print("Optimizacija funkcije f6 binarni")
g6 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
g6.run(f6, steps=10000, print_every=500)


chromosome = "float"
crossover_fn = "arithmetic"
print("Optimizacija funkcije f7 s pomicnom tockom")

g6 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
g6.run(f7, steps=10000, print_every=500)

chromosome = "binary"
crossover_fn = "uniform"
print("Optimizacija funkcije f7 binarni")
g6 = GeneticAlgorithm(n, chromosome, lower_limit, upper_limit, dimension, crossover_fn, b, precision, pm, 1)
g6.run(f6, steps=10000, print_every=500)
