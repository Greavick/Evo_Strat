from math import pi, cos, sqrt, exp
import matplotlib.pyplot as plt
import pandas as pd
import random
import operator


class Individual:
    def __init__(self,
                 a=random.gauss(0, 1),
                 b=random.gauss(0, 1),
                 c=random.gauss(0, 1),
                 a_var=random.gauss(0, 1),
                 b_var=random.gauss(0, 1),
                 c_var=random.gauss(0, 1)):
        self.a = a
        self.b = b
        self.c = c
        self.a_var = a_var
        self.b_var = b_var
        self.c_var = c_var
        self.r = random.gauss(0, 1)
        self.fitness = self.eval()

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
    next_gen = sorted(offspring, key=operator.attrgetter('fitness'), reverse=True)[0:len(parents)]
    return next_gen


def select_pop_plus(mi, parents, offspring):
    next_gen = sorted(parents + offspring, key=operator.attrgetter('fitness'), reverse=True)[0:len(parents)]
    return next_gen


def discrete_crossover(pop, mi):
    x = 0
    off = []
    for i in range(mi):
        p1 = pop[x]
        p2 = pop[x-1]
        r_select = [p1 if random.uniform(0, 1) > 0.5 else p2 for _ in range(6)]
        off.append(Individual(r_select[0].a,
                              r_select[1].b,
                              r_select[2].c,
                              r_select[3].a_var,
                              r_select[4].b_var,
                              r_select[5].c_var))
        x += 1
        if x >= len(pop):
            x -= len(pop)
    return off


def intermediate_crossover(pop, mi):
    x = 0
    off = []
    for i in range(mi):
        p1 = pop[x]
        p2 = pop[x-1]
        off.append(Individual((p1.a + p2.a) / 2,
                              (p1.b + p2.b) / 2,
                              (p1.c + p2.c) / 2,
                              (p1.a_var + p2.a_var) / 2,
                              (p1.b_var + p2.b_var) / 2,
                              (p1.c_var + p2.c_var) / 2))
        x += 1
        if x >= len(pop):
            x -= len(pop)
    return off


def gen_offspring(pop, mi):
    x = 0
    off = []
    tau1 = 1 / sqrt(2 * len(pop))
    tau2 = 1 / sqrt(2 * sqrt(len(pop)))
    for i in range(mi):
        p = pop[x]
        off.append(Individual(p.a + random.gauss(0, 1) * p.a_var,
                              p.b + random.gauss(0, 1) * p.b_var,
                              p.c + random.gauss(0, 1) * p.c_var,
                              p.a_var * exp(p.r * tau1) * exp(random.gauss(0, 1) * tau2),
                              p.b_var * exp(p.r * tau1) * exp(random.gauss(0, 1) * tau2),
                              p.c_var * exp(p.r * tau1) * exp(random.gauss(0, 1) * tau2)))
        x += 1
        if x >= len(pop):
            x -= len(pop)
    return off


def run(max_gen=100, pop_size=10, mi=20, file_path="model15.txt"):

    data = pd.read_csv(file_path, delimiter=",")
    global X, Y
    X = data["x"]
    Y = data["y"]

    err = []
    pop = init_pop(pop_size)
    eval_pop(pop)
    t = 0

    while t < max_gen:
        # offspring = intermediate_crossover(pop, mi)
        offspring = pop
        offspring = gen_offspring(offspring, mi)
        eval_pop(offspring)
        pop = select_pop_plus(mi, pop, offspring)
        # pop = select_pop(mi, pop, offspring)
        t = t + 1
        err.append(pop[0].fitness)
        print(t)

    yy = []
    p = pop[0]

    print("Final Parameters: \na={}\nb={}\nc={}".format(p.a, p.b, p.c))
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


run()
