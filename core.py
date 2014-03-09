__author__ = 'Michal'
import random
from multiprocessing import Pool as ThreadPool

class Individual:
    def __init__(self, chromosome=None, chance_of_repr=0.7, chance_of_mutation=0.1):
        self.chromosome = chromosome
        self.__chance_of_repr = chance_of_repr
        self.__chance_of_mutation = chance_of_mutation
        self.rating = None

    def crossover(self, other):
        if random.random() < self.__chance_of_repr:
            (chromosome1, chromosome2) = self.__cross_over(self, other)
            return (Individual(chromosome1), Individual(chromosome2))
        return None

    def mutate(self):
        if random.random() < self.__chance_of_mutation:
            self.__mutate()

    def __cross_over(self, other):
        random.seed(self.chromosome)
        point = random.randint(0, len(self.chromosome)-1)
        pair = (
            self.chromosome[:point] + other.chromosome[point:],
            other.chromosome[:point] + self.chromosome[point:],
        )
        return pair #krzyżowanie

    def __mutate(self):
        mutated = []
        original = self.__chromosome # do lokalnej zmiennej dla lepszej czytelności

        for i in range(len(original) - 1):
            if not random.random() < self.__chance_of_mutation: # szansa, że NIE zostanie zmutowany
                mutated[i] = original[i] # przepisz
            else: # przepisz zamienione miejscami
                mutated[i] = original[i + 1]
                mutated[i + 1] = original[i]
        self.__chromosome = mutated # podmień na zmutowany chromosom


class Roulette:
    def __init__(self, list):#list = uporządkowana tablica osobników
        self.__list = list
        spectrum = list[0].rating - list[-1].rating
        self.__dict = {}
        last = 0
        for elem in list:
            curr = elem.rating/spectrum - last
            dict[(last, curr)] = elem

    def next(self):#zwraca PARĘ
        while True:
            val1, val2 = None, None
            while val1 is val2:#upewnij się, że wylosowana para to dwa różne osobniki
                val1, val2 = self.__next(), self.__next()
            yield val1, val2

    def __next(self):
        val = random.random
        for k in self.__dict.keys():
            if k[0] <= val <= k[1]:
                return self.__dict[k]


class Population:
    def __init__(self, function, population_size=100, cities=5):
        self.__size = population_size
        self.population = self.__init_generate_population(cities)
        self.evaluate()
        self.__size = population_size
        self.__fcn = function

    def __init_generate_population(self, cities): #wygeneruj pierwsze pokolenie rozwiązań
        for i in range(self.__size):
            list = range(cities) #lista indeksów miast
            chr = [] #chromosom
            for j in range(cities):#dla każdego miasta
                index = random.randint(len(list))#losuj indeks miasta
                chr.append(list[index]) #dodaj miasto do chromosomu
                del list[index]#usuń miasto z listy
            self.population.append(Individual(chr))

    def evaluate(self):
        for indiv in self.population:
            indiv.rating = self.__fcn(indiv.chromosome)
        self.population.sort(key=lambda indiv: indiv.rating)
        self.fittest = self.population[0]

    def crossover(self):
        new_population = []
        while len(new_population) < self.__size:
            i = int(abs(random.gauss(0, 0.3)*100))
            i = i if i < self.__size else self.__size - 1
            j = int(abs(random.gauss(0, 0.3)*100))
            j = j if j < self.__size else self.__size - 1
            child1, child2 = self.population[i].crossover(self.population[j])
            if child1 is None: #wystarczy sprawdzić jedno dziecko
                continue
            new_population.append(child1)
            new_population.append(child2)
        self.population = new_population

    def mutation(self): # tu tylko wywołanie metody z Individual
        for indiv in self.population:
            indiv.mutate()

    def selection(self):
        roulette = Roulette(self.population)
        self.__mating_pool = []
        while len(self.__mating_pool) < 99:


