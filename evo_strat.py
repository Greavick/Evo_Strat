from math import pi, cos, sqrt, exp
import matplotlib.pyplot as plt
import pandas as pd
import random
import operator

t = 0
max_gen = 100
pop_size = 100
mi = 80
data = pd.read_csv("model15.txt", delimiter=",")
X = data["x"]
Y = data["y"]
tau1 = 1 / sqrt(2 * pop_size)
tau2 = 1 / sqrt(2 * sqrt(pop_size))


class Individual:
    def __init__(self,
                 a=random.gauss(0, 1),
                 b=random.gauss(0, 1),
                 c=random.gauss(0, 1),
                 a_var=random.gauss(0, 1),
                 b_var= random.gauss(0, 1),
                 c_var= random.gauss(0, 1)):
        self.a = a
        self.b = b
        self.c = c
        self.a_var = a_var
        self.b_var = b_var
        self.c_var = c_var
        self.r = random.gauss(0, 1)
        self.fitness = -1

    def set_args(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def eval(self):
        self.fitness = 1 / sum([abs(Y[i] - origin_function(self.a, self.b, self.c, X[i])) for i in range(len(X))])
        return 0


def origin_function(a, b, c, x):
    return a * (x ** 2 - b * cos(c * pi * x))


def init_pop(pop_size):
    pop = []
    for i in range(pop_size):
        pop.append(Individual())
    return pop


def eval_pop(pop):
    for i in range(len(pop)):
        pop[i].eval()


def select_pop(mi, parents, offspring):
    off = sorted(offspring, key=operator.attrgetter('fitness'), reverse=True)[0:mi]
    par = parents[0:pop_size-mi]
    next_gen = par + off
    next_gen = sorted(next_gen, key=operator.attrgetter('fitness'), reverse=True)
    print(next_gen[0].fitness)
    return next_gen


def select_pop_plus(mi, parents, offspring):
    xx = sorted(parents + offspring, key=operator.attrgetter('fitness'), reverse=True)[0:mi]
    print(xx[0].fitness)
    print(xx[10].fitness)
    return xx


def gen_offspring(pop):
    return [Individual(p.a + random.gauss(0, 1) * p.a_var,
                       p.b + random.gauss(0, 1) * p.b_var,
                       p.c + random.gauss(0, 1) * p.c_var,
                       p.a_var * exp(p.r * tau1) * exp(random.gauss(0, 1) * tau2),
                       p.b_var * exp(p.r * tau1) * exp(random.gauss(0, 1) * tau2),
                       p.c_var * exp(p.r * tau1) * exp(random.gauss(0, 1) * tau2), )
            for p in pop]


err = []
pop = init_pop(pop_size)
eval_pop(pop)

while t < max_gen:
    offspring = gen_offspring(pop)
    eval_pop(offspring)
    # pop = select_pop_plus(pop_size, pop, offspring)
    pop = select_pop(mi, pop, offspring)
    t = t + 1
    err.append(pop[0].fitness)
    print(t)

yy = []
p = pop[0]
for x in X:
    yy.append(origin_function(p.a, p.b, p.c, x))

plt.subplot(1, 2, 1)
plt.title("Fitness over Time")
plt.plot(err)
plt.ylabel('Fitness')
plt.xlabel('Generation')
plt.subplot(1, 2, 2)
plt.title("Final Graph Approximation")
plt.plot(X, Y)
plt.plot(X, yy)
plt.show()






