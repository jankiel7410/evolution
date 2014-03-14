__author__ = 'Michal'
import random
from multiprocessing import Pool as ThreadPool

class Individual:
    def __init__(self, chromosome=None, mutation_chance=0.1):
        self.chromosome = chromosome

        self.m_chance = mutation_chance
        self.rating = None

    def crossover(self, other):
        chromosome1, chromosome2 = self.__cross_over(self, other)
        return Individual(chromosome1, mutation_chance=self.m_chance), Individual(chromosome2,mutation_chance=self.m_chance)

    def mutate(self):
        if random.random() < self.m_chance:
            self.__mutate()

    def __cross_over(self, other):#krzyżowanie chromosomów
        point = random.randint(0, len(self.chromosome)-1)
        p1 = self.chromosome[:point] + other.chromosome[point:]
        p2 = other.chromosome[:point] + self.chromosome[point:]

        return p1, p2

    def __mutate(self):
        mutated = []
        original = self.__chromosome # do lokalnej zmiennej dla lepszej czytelności

        for i in range(len(original) - 1):
            if not random.random() < self.m_chance: # szansa, że NIE zostanie zmutowany
                mutated[i] = original[i] # przepisz
            else: # przepisz zamienione miejscami
                mutated[i] = original[i + 1]
                mutated[i + 1] = original[i]
        self.chromosome = mutated # podmień na zmutowany chromosom

    def is_valid(self):
        import collections
        counted_occurrrences = collections.Counter(self.chromosome) # {element: liczba_wystąpień}
        doubled = [key for key in counted_occurrrences if counted_occurrrences[key] > 1] # dodaj do tablicy doubled jeżeli występuje więcej niż raz
        return doubled == [] # zwraca true, jeżeli nie znalazł żadnych ddublujących się elementów


class Roulette:
    def __init__(self, individuals):#list = uporządkowana tablica osobników
        self.max = sum(1/indiv.rating for indiv in individuals)
        self.individuals = individuals

    def next(self):#źle, największą szansę ma teraz koleś, który ma najdłuższą trasę
        pick = random.uniform(0, self.max)#losuj liczbę z zakresu (0, suma z długości tras)
        current = 0
        for individual in self.individuals:
            current += 1/individual.rating
            if current > pick:
                return individual


class Population:
    def __init__(self, function, pop_size=100, number_of_cities=5, repr_chance=0.2, mutation_chance=0.1, generations=100):
        self.offspring = []
        self.m_chance = mutation_chance
        self.repr_chance = repr_chance
        self.size = pop_size
        self.__fcn = function
        self.most_fitted = None
        self.population = []
        self.__init_generate(number_of_cities)
        self.evaluate()

    def __init_generate(self, number_of_cities): #wygeneruj pierwsze pokolenie rozwiązań
        indexes = list(range(number_of_cities)) #lista indeksów miast
        for i in range(self.size):
            chromosome = indexes[:] #chromosom, na razie kopia indexes
            random.shuffle(chromosome) # poprzestawiaj elementy w losowej kolejności
            self.offspring.append(Individual(chromosome, mutation_chance=self.m_chance))

    def evaluate(self):
        for indiv in self.offspring:
            indiv.rating = self.__fcn(indiv.chromosome)

    def crossover(self):#fucking nope
        offspring = []
        roulette = Roulette(self.population)
        while len(offspring) < self.size*self.repr_chance:
            parent1, parent2 = roulette.next(), roulette.next()#losuj ruletką rodziców
            if parent1 is parent2:#nie chcemy klonów
                continue
            child1, child2 = parent1.crossover(parent2)
            if child1.is_valid():
                offspring.append(child1)
            if child2.is_valid():
                offspring.append(child2)

        self.offspring = offspring

    def mutation(self): # tu tylko wywołanie metody z Individual
        for indiv in self.population:
            indiv.mutate()

    def selection(self):
        roulette = Roulette(sorted(self.population + self.offspring))#ruletka z całości
        selected = [roulette.next() for i in range(self.size)] # losowane elementy, które znajdą się w kolejnej populacji
        selected.sort(key=lambda indiv: indiv.rating) # od najlepszego do najgorszego
        self.population = selected
        if selected[0].rating > self.most_fitted:
            self.most_fitted = selected[0].rating

    def iterate(self):
        pass

class InfoGrabber:
    def __init__(self):
        self.most_fitted = []
        self.least_fitted = []
        self.avg = []

    def grab_info(self, population): # wykonywane przy każdej iteracji daje info nt. przebiegu obliczania rozwiązania
        fittest = min(population.offspring, key=lambda indiv: indiv.rating) # najlepszy z nowego pokolenia, czyli najkrótsza trasa
        self.most_fitted.append(fittest)
        least_fitted = max(population.offspring, key=lambda indiv: indiv.rating) #najgorszy osobnik to ten z najdłuższą trasą
        self.least_fitted.append(least_fitted)
        rating_sum = sum(indiv.rating for indiv in population.population)
        self.avg = rating_sum / population.size



