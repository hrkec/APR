import numpy as np

from chromosome import BinaryChromosome
from chromosome import FloatChromosome


class GeneticAlgorithm:
    def __init__(self, n, chromosome, ll, ul, degree, crossover_fn, b, precision,
                 pm, probabilities, a=1e-4):
        self.n = n
        if chromosome == "binary":
            self.population = [
                BinaryChromosome(ll, ul, precision, degree, pm, crossover_fn) for _ in range(self.n)
            ]
        elif chromosome == "float":
            self.population = [
                FloatChromosome(ll, ul, degree, pm, b, crossover_fn) for _ in range(self.n)
            ]
        else:
            raise ValueError("Wrong chromosome type - can only be 'binary' or 'float'")

        if probabilities == 1:
            self.probabilities_fn = lambda: self.probabilities(a)
        elif probabilities == 2:
            self.probabilities_fn = lambda: self.probabilities2(a)
        else:
            raise ValueError("Wrong probabilities")

    def probabilities(self, a):
        prob = np.copy(self.vals)
        max_ = np.max(prob)
        prob = (max_ - prob + a) / max_
        prob /= np.sum(prob)
        return prob

    def probabilities2(self, a):
        prob = np.copy(self.vals)
        prob = np.exp(a * prob - np.max(a * prob))
        prob /= np.sum(prob)
        return prob

    def gga(self, f, step, max_steps):
        elements = np.random.choice(self.population, size=2 * (self.n - 2), replace=True, p=self.probabilities_fn())
        self.population[-1] = self.population[np.argmin(self.vals)]
        self.population[-2] = self.population[-1].mutate(step, max_steps)
        for i in range(self.n - 2):
            a = elements[2 * i]
            b = elements[2 * i + 1]
            self.population[i] = a.crossover(b).mutate(step, max_steps)

        self.vals = np.array([f(x.evaluate()) for x in self.population]).ravel()

    def run(self, f, steps=500, print_every=100):
        self.vals = np.array([f(x.evaluate()) for x in self.population]).ravel()
        best = [np.min(self.vals)]
        for i in range(steps):
            if print_every != 0 and i % print_every == 0:
                self.my_print(f, i)
            self.gga(f, i, steps)
            best.append(np.min(self.vals))
            p = np.argmin(self.vals)
            if print_every != 0 and self.vals[p] < 10e-12:
                print("Minimum pronaden u iteraciji ", i)
                print(self.population[p].evaluate(), self.vals[p])
                return best
        if print_every != 0:
            self.my_print(f, steps)
        return best

    def best_value(self):
        p = np.argmin(self.vals)
        return self.vals[p]

    def my_print(self, f, step=None):
        if step is not None:
            print("Iteracija: ", step)
            p = np.argmin(self.vals)
            print("\t", self.population[p].evaluate(), self.vals[p])
