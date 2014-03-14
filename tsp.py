__author__ = 'jankiel'
import random
import math

#dystans pomiedzy dwoma miastami


def get_dist(p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx**2 + dy**2)


class Troll:
    def __init__(self, points):
        self.first = points[0]#pierwsze miasto zawsze jest pierwszym miastem
        self.points = points[1:]

    def rate_solution(self):
        total_dist = 0
        total_dist += get_dist(self.first, self.points[-1])#dystans pomiędzy pierwszym a ostatnim
        curr = self.first
        for p in self.points:
            total_dist += get_dist(curr, p)
            curr = p