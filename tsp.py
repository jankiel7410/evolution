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
    print(dist_sum)
