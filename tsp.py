__author__ = 'jankiel'
import random
import math

#dystans pomiedzy dwoma miastami


class Troll:

    def __init__(self, points):
        self.points = points

    def get_distance(self, p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx**2 + dy**2)

    def rate_solution(self):
        pass