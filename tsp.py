__author__ = 'jankiel'
import random
import math

#dystans pomiedzy dwoma miastami


def get_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx**2 + dy**2)


def rate_solution(points):
    dist_sum = 0
    for i in range(0, len(points)):
        dist_sum += get_distance(points[i - 1], points[i])
    return dist_sum

#[(30, 100), (120, 130), (210, 50), (360, 300), (100, 250)]
#b = [(300, 100), (120, 13), (210, 50), (360, 300), (10, 250)]
def solve_bruteforce(cities):#bruteforce4life
    import itertools
    solutions = list(itertools.permutations(cities[1:]))
    solutions = list(map(lambda x: (cities[0], )+x, solutions))
    rates = [rate_solution(points) for points in solutions]
    zipped = list(zip(rates, solutions))
    zipped.sort(key=lambda x: x[0])
    print(zipped)

