from copy import deepcopy
from functools import reduce

import numpy as np


class Chromosome:
    def crossover(self, other):
        pass

    def mutate(self, step=None):
        pass

    def evaluate(self):
        pass


class FloatChromosome(Chromosome):
    def __init__(self, ll, ul, degree, pm, b, crossover_function):
        self.ll = ll
        self.ul = ul
        self.degree = degree
        self.data = np.random.uniform(self.ll, self.ul, size=self.degree)
        self.pm = pm
        self.b = b
        self.crossover_function = crossover_function

    def crossover(self, other):
        if self.crossover_function == "arithmetic":
            return self.arithmetic_crossover(other)
        if self.crossover_function == "heuristic":
            return self.heuristic_crossover(other)

    def arithmetic_crossover(self, other):
        child = deepcopy(self)
        alpha = np.random.uniform(size=self.data.shape)
        child.data = alpha * self.data + (1 - alpha) * other.data
        #  child.data = (self.data + other.data) / 2
        return child

    def heuristic_crossover(self, other):
        child = deepcopy(self)
        alpha = np.random.uniform(size=self.data.shape)
        if self.evaluate() < other.evaluate():
            b = self
            a = other
        else:
            b = other
            a = self
        child.data = b.data + alpha * (b.data - a.data)
        return child

    def mutate(self, step=None, max_step=None):
        res = deepcopy(self)
        if np.random.uniform(size=1) < self.pm:
            r = 1 - np.random.uniform(size=1)**(1-step/max_step)**self.b
            noise = (self.ul - self.ll) * np.random.uniform(-r, r, size=self.degree)
            res.data = np.clip(res.data + noise, self.ll, self.ul)
        return res

    def evaluate(self):
        return self.data


class BinaryChromosome(Chromosome):
    def __init__(self, ll, ul, precision, degree, pm, crossover_function):
        self.ll = ll
        self.ul = ul
        self.precision = precision
        self.degree = degree
        self.n = np.int(np.ceil(np.log2(np.floor(1+(self.ul-self.ll) * 10**precision))))
        self.data = np.random.randint(2, size=[degree, self.n])
        self.crossover_function = crossover_function
        self.pm = pm

    def crossover(self, other):
        if self.crossover_function == "uniform":
            return self.uniform_crossover(other)

    def uniform_crossover(self, other):
        child = deepcopy(self)
        child.data = np.where(np.random.uniform(size=self.data.shape), self.data, other.data)
        return child

    def mutate(self, step=None, max_step=None):
        res = deepcopy(self)
        res.data = np.where(np.random.uniform(size=(self.degree, self.n)) < self.pm, 1 - self.data, self.data)
        return res

    def evaluate(self):
        return self.ll + (self.ul - self.ll) * reduce(lambda a, b: 2*a + b, self.data.T) / (2 ** self.n - 1)
