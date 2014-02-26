__author__ = 'Michal'
import random

class Individual:
    def __init__(self, chromosome, fenotype=None):
        self.__chromosome = chromosome
        self.__fenotype = lambda arg: fenotype(chromosome, arg) if fenotype else None

    def produce_child(self, other):
        chromosome = self.__cross_over(other)
        return Individual(chromosome, self.fenotype)

    def solve(self, arg):
        return self.__fenotype(arg)

    def __cross_over(self, other):
        random.seed(self.chromosome)
        point = random.randint(0, len(self.chromosome)-1)
        return self.chromosome[:point] + other.chromosome[point:]
