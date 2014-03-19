# -*- coding: UTF-8 -*-
from math import sqrt

__author__ = 'jankiel'
import math

#dystans pomiedzy dwoma miastami


def get_dist(p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx**2 + dy**2)


class TSP:
    def __init__(self, points):
        self.points = points
        self.p = None

    def rate_solution(self, array):
        total_dist = sum([get_dist(self.points[array[i]], self.points[array[i+1]]) for i in range(len(array) - 1)])
        total_dist += get_dist(self.points[array[0]], self.points[array[-1]])
        return total_dist

    def evaluate(self, pop_size, repr_chance, mutation_chance, generations, show=True):

        if show:
            self.with_chart(pop_size, repr_chance, mutation_chance, generations)
        else:
            self.avg(pop_size, repr_chance, mutation_chance, generations)

    def show(self):
        import matplotlib.pyplot as plt
        results = plt.figure()
        ax1 = results.add_subplot(111)

        ax1.plot(self.p.info_grabber.avg, label='average', color='black', linewidth=1)
        ax1.plot([x.rating for x in self.p.info_grabber.most_fitted], label='fittest', color='red', linewidth=1)
        ax1.plot([x.rating for x in self.p.info_grabber.least_fitted], label='least fitted', color='blue', linewidth=1)
        ax1.plot([x.rating for x in self.p.info_grabber.most_fitted_pop], label='local fittest', color='green', linewidth=1)
        ax1.legend()
        road = plt.figure()
        ax2 = road.add_subplot(111)
        points = self.points
        indexes = self.p.most_fitted.chromosome
        newp=[]
        for i in indexes:
            newp.append(points[i])

        entire = sum([get_dist(newp[i], newp[i+1]) for i in range(len(newp) - 1)])
        entire += get_dist(newp[0], newp[-1])
        newp.append(newp[0])

        print(
            'sprawdz sume',
            entire,
              )

        x, y = zip(*newp)

        ax2.plot(y, x, marker='o', ls=' ', color='red')
        ax2.plot(y, x, color='blue')

        plt.show()

    def with_chart(self, pop_size, repr_chance, mutation_chance, generations):
        import core
        self.p = core.Population(self.rate_solution,
                            len(self.points),
                            pop_size=pop_size,
                            repr_chance=repr_chance,
                            mutation_chance=mutation_chance,
                            generations=generations)
        import time
        start = time.time()
        self.p.iterate()
        stop = time.time()
        print('obliczono trasę w czasie %d sekund' % (stop-start))
        print('obliczona trasa ma długość: %d' % self.p.most_fitted.rating)
        self.show()

    def avg(self, pop_size, repr_chance, mutation_chance, generations):
        import core
        results = []
        import time
        start = time.time()
        for _ in range(10):
            self.p = core.Population(self.rate_solution,
                            len(self.points),
                            pop_size=pop_size,
                            repr_chance=repr_chance,
                            mutation_chance=mutation_chance,
                            generations=generations)
            results.append(self.p.iterate().rating)
        avg = sum(results)/len(results)
        dev = sum([(x - avg)**2 for x in results])/len(results)
        dev = sqrt(dev)
        stop = time.time()
        print('obliczono 10 iteracji w czasie %d sekund' % (stop-start))
        print('srednia, odchylenie: %d, %d' % (avg, dev))

    def alternative_method(self, iterations):
        import random
        from core import Individual
        indexes = list(range(len(self.points)))
        chromosome = indexes[:]
        random.shuffle(chromosome)
        best = Individual(indexes, chromosome)
        best.rating = self.rate_solution(best.chromosome)
        import time
        start = time.time()
        for i in range(iterations):
                chromosome = indexes[:] #chromosom, na razie kopia indexes
                random.shuffle(chromosome) # poprzestawiaj elementy w losowej kolejności
                indv = Individual(indexes, chromosome)
                indv.rating = self.rate_solution(indv.chromosome)
                best = indv if indv.rating < best.rating else best
        print(best.rating, ' in ', time.time()-start)