# -*- coding: UTF-8 -*-
__author__ = 'Michal'
import random


class Individual:
    def __init__(self, valid_genome, chromosome=None, mutation_chance=0.1):
        self.chromosome = chromosome
        self.valid_genome = valid_genome
        self.m_chance = mutation_chance
        self.__repair()
        self.rating = None

    def crossover(self, other):

        chromosome1, chromosome2 = self.__cross_over(other)
        i1 = Individual(self.valid_genome, chromosome1, self.m_chance)
        i2 = Individual(self.valid_genome, chromosome2, self.m_chance)
        return i1, i2

    def mutate(self):
        if random.random() < self.m_chance:
            self.__mutate()
            #self.__repair()

    def __cross_over(self, other):#krzyżowanie chromosomów
        p1, p2 = self.cross_over_chromosomes(self.chromosome, other.chromosome)
        return p1, p2

    @staticmethod
    def cross_over_chromosomes(ch1, ch2):#krzyżowanie chromosomów 29216.4532612964 27748.70957813485
        i = random.randint(0, len(ch1) - 2)
        j = random.randint(i+1, len(ch1) - 1)
        #dla pierwszego dziecka
        middle = ch1[i:j]#pobierz kawalek genomu rodzica 1
        tmp = [x for x in ch2 if x not in middle]#wyrzuc z genomu 2 geny wystepujace w middle
        start, end = tmp[:i], tmp[i:] # podziel pozostalosc genomu 2 na 2 czesci pasujace do genomu 1
        child1 = start + middle + end # polacz czesci razem
        #dla drugiego dziecka
        middle = ch2[i:j]
        tmp = [x for x in ch1 if x not in middle]
        start, end = tmp[:i], tmp[i:]
        child2 = start + middle + end
        return child1, child2

    def __mutate(self):
        i = random.randint(0, len(self.chromosome) - 2)
        j = random.randint(i+1, len(self.chromosome) - 1)
        center = self.chromosome[i:j]
        center.reverse()
        self.chromosome = self.chromosome[:i] + center + self.chromosome[j:]

    def __repair(self):
        import collections
        counted_occurrrences = collections.Counter(self.chromosome) # {element: liczba_wystąpień}
        doubled = {key: counted_occurrrences[key] for key in counted_occurrrences if counted_occurrrences[key] > 1} # dodaj do tablicy doubled jeżeli występuje więcej niż raz
        if not doubled:
            return
        keys = list(doubled.keys())
        for i in self.valid_genome:
            if i in self.chromosome:#jeżeli i jest w chromosomie, to wszystko w porządku, idź dalej
                continue

            self.chromosome[self.chromosome.index(keys[-1])] = i#podmień i za powtarzający się genom
            doubled[keys[-1]] -= 1 # jedno powtórzenie mniej
            if doubled[keys[-1]] == 1:#jeżeli zostało jedno powtórzenie genomu z doubled
                del doubled[keys[-1]]#wyrzuć go ze słownika powtarzających się
                del keys[-1]#wyrzuć go z kluczy


def key_cfn(indv):
    return indv.rating


class Tournament:
    def __init__(self, individuals, delete=False):#list = uporządkowana tablica osobników
        self.indv = individuals[:]
        self.delete = delete

    def next(self):
        group = [self.indv[random.randint(0, len(self.indv)-1)] for _ in range(3)]
        best = min(group, key=key_cfn)
        if self.delete:
            del self.indv[self.indv.index(best)]
        return best


class Roulette:
    def __init__(self, individuals):#list = uporządkowana tablica osobników
        max_rating = individuals[-1].rating
        sum_rating = sum([max_rating - i.rating for i in individuals])
        #[sum([(max - j + 1)/(wat + 1) for j in a[:i+1]]) for i in range(len(a))]
        self.probs = [sum([(max_rating - j.rating + 1)/(sum_rating + 1) for j in individuals[:i+1]])
                      for i in range(len(individuals))] # suma prawdopodob.
        self.individuals = {self.probs[i]: individuals[i] for i in range(len(individuals))}

    def next(self):
        pick = random.uniform(0, self.probs[-1])#losuj liczbę z zakresu (0, suma z długości tras)
        from bisect import bisect
        index = bisect(self.probs, pick)
        if index < 0 or index >= len(self.probs):
            raise Exception('Roulette.next bisect: out of range index=%d'%index)
        return self.individuals[self.probs[index]]


class Population:
    def __init__(self, function, number_of_cities, pop_size=100, repr_chance=0.2, mutation_chance=0.1, generations=100):
        self.offspring = []
        self.generations = generations
        self.m_chance = mutation_chance
        self.repr_chance = repr_chance
        self.size = pop_size
        self.__fcn = function
        self.most_fitted = None
        self.population = []
        self.__init_generate(number_of_cities)
        self.evaluate()
        self.population = self.offspring
        self.info_grabber = None

    def __init_generate(self, number_of_cities): #wygeneruj pierwsze pokolenie rozwiązań
        indexes = list(range(number_of_cities)) #lista indeksów miast
        for i in range(self.size):
            chromosome = indexes[:] #chromosom, na razie kopia indexes
            random.shuffle(chromosome) # poprzestawiaj elementy w losowej kolejności
            self.offspring.append(Individual(indexes, chromosome, mutation_chance=self.m_chance))

    def evaluate(self):
        for indiv in self.offspring:
            indiv.rating = self.__fcn(indiv.chromosome)

    def crossover(self):
        offspring = []
        roulette = Tournament(self.population)
        i = 0
        while len(offspring) < self.size*self.repr_chance:
            parent1, parent2 = roulette.next(), roulette.next()#losuj ruletką rodziców
            i+=1
            if i > 1000:
                raise Exception('to coś nowego', len(['' for i in self.population if i.rating == parent1.rating]))
            if parent1 is parent2:#nie chcemy klonów
                continue
            child1, child2 = parent1.crossover(parent2)

            offspring.append(child1)
            offspring.append(child2)

        self.offspring = offspring

    def mutation(self): # tu tylko wywołanie metody z Individual
        for indiv in self.offspring:
            indiv.mutate()

    def selection(self):
        roulette = Tournament(self.population + self.offspring, delete=True)#ruletka z całości
        selected = [roulette.next() for _ in range(self.size)]
        self.population = selected
        best = min(selected, key=key_cfn)
        if best.rating < self.most_fitted.rating:
            self.most_fitted = best

    def iterate(self):
        self.info_grabber = InfoGrabber()
        self.info_grabber.get_most_fitted_pop(self.population)
        self.most_fitted = self.info_grabber.most_fitted_pop[0]
        self.info_grabber.get_most_fitted(self.most_fitted)
        self.info_grabber.get_least_fitted(self.population)

        for i in range(self.generations):
            self.crossover()
            self.mutation()
            self.evaluate()
            self.selection()
            self.info_grabber.get_most_fitted_pop(self.population)
            self.info_grabber.get_avg(self.population)
            self.info_grabber.get_least_fitted(self.population)
            self.info_grabber.get_most_fitted(self.most_fitted)
        return self.most_fitted


class InfoGrabber:
    def __init__(self):
        self.most_fitted = []
        self.most_fitted_pop = []
        self.least_fitted = []
        self.avg = []

    def get_most_fitted_pop(self, individuals):
        fittest = min(individuals, key=key_cfn) # najlepszy z nowego pokolenia, czyli najkrótsza trasa
        self.most_fitted_pop.append(fittest)

    def get_least_fitted(self, individuals):
        fittest = max(individuals, key=key_cfn) # najlepszy z nowego pokolenia, czyli najkrótsza trasa
        self.least_fitted.append(fittest)

    def get_avg(self, individuals):
        rating_sum = sum(indiv.rating for indiv in individuals)
        self.avg.append(rating_sum / len(individuals))

    def get_most_fitted(self, individual):
        self.most_fitted.append(individual)

if __name__ == "__main__":
    from random import shuffle
    v =[0,1,2,3, 4]#1843
    indvs = []
    import tsp
    t = tsp.TSP([(11, 26), (41, 9), (73, 28), (58, 46), (29, 42), (0,0)])
    for i in range(100):
        c = v[:]
        shuffle(c)
        indiv = Individual(v, c)
        indiv.rating = t.rate_solution(c)
        indvs.append(indiv)
    indvs.sort(key=lambda x: x.rating)
    from matplotlib import pyplot as plt
    lol = []
    r = Tournament(indvs, delete=False)
    for i in range(100):
        lol.append(r.next())
    import collections
    occ = collections.Counter(lol)
    ll = [(k, occ[k]) for k in occ if k is not None or k.rating is not None]
    print(len(ll))
    keys, vals = zip(*ll)
    vals = list(vals)
    x = [int(i.rating) for i in keys]
    print(len(vals))
    copy = vals[:]
    vals.sort(key=lambda wat:  x[copy.index(wat)])
    x.sort()
    plt.plot(x, vals, marker='o', ls='')
    # add some
    plt.show()