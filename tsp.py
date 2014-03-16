# -*- coding: UTF-8 -*-
__author__ = 'jankiel'
import math

#dystans pomiedzy dwoma miastami


def get_dist(p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx**2 + dy**2)


class TSP:
    def __init__(self, points):
        self.first = points[0]#pierwsze miasto zawsze jest pierwszym miastem
        self.points = points[1:]

    def rate_solution(self, array):
        total_dist = 0
        total_dist += get_dist(self.first, self.points[-1])#dystans pomiędzy pierwszym a ostatnim
        curr = self.first
        for index in array:
            total_dist += get_dist(self.points[index], curr)
            curr = self.points[index]
        return total_dist

    def evaluate(self):
        import core
        p = core.Population(self.rate_solution,
                            len(self.points),
                            pop_size=200,
                            repr_chance=0.4,
                            mutation_chance=0.01,
                            generations=500)
        import time
        start = time.time()
        p.iterate()
        stop = time.time()
        print('obliczono trasę w czasie %d sekund' % (stop-start))
        print('obliczona trasa ma długość: %d' % p.most_fitted.rating)
        import matplotlib.pyplot as plt
        plt.plot(p.info_grabber.avg, label='average', color='black', linewidth=2)
        plt.plot([x.rating for x in p.info_grabber.most_fitted], label='fittest', color='red', linewidth=2)
        plt.plot([x.rating for x in p.info_grabber.least_fitted], label='least fitted', color='blue', linewidth=2)
        plt.plot([x.rating for x in p.info_grabber.most_fitted_offspring], label='fittest in offspring', color='green', linewidth=2)
        plt.legend()
        plt.show()
