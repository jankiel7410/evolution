__author__ = 'Michal'

import ploter, core, tsp

def solve():
    m = ploter.MapCreator2000()
    cities = m.points
    pop = core.Population(tsp.rate_solution, cities=len(cities))


if __name__ == "__main__":
    solve()