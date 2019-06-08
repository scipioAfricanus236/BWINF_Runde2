from new_breeding import Breeding
from findBestSequence import FindBestSequence


import random
import numpy as np 
import time
import logging

import sys 
sys.path.append("/Users/juliuside/Desktop/BWINF_Runde2/Aufgabe2")
import HelperMethods as hm

class Population:
    def __init__(self, triangles, population_size, treshold, time=None, add=0):
        """
            input: - population_size = integer representing the size of the populations
                   - triangles = list of the smallest angle and largest edge of each triangle
        """
        #making sure that the input has the right type and format
        if (type(population_size) is int) == False or population_size <= 0:
            raise ValueError("population_size has to be a positive integer: {}".format(population_size))
        invalid_elements = [i for i in triangles if len(i) != 3 or (type(i[0]) is int) == False or (type(i[1]) is int) == False]
        if invalid_elements:
            raise ValueError("Wrong input, every elements has to have the value of the smallest angle and the largest edge and the edges.")
        if (type(population_size) is int) == False or population_size <= 0:
            raise ValueError("Wrong input for population_size: {}, has to be an int value".format(population_size)) 
        if (type(treshold) is float) == False or treshold <= 0:
            raise ValueError("treshold has to be a positive float value: {}".format(treshold))

        self.first_population = list(self.generateSequences(population_size, triangles))
        self.check(triangles, self.first_population)
        self.triangles = triangles
        self.population_size = population_size
        self.treshold = treshold
        self.time = time
        self.add = add

    @property
    def optimizedIndividual(self):
        current_time = time.time()
        if self.time == None:
            timeStamp = None
        else:
            timeStamp = [current_time, self.time]

        self.next_generation(self.first_population, self.treshold, timeStamp)
        
        return self.peak

    def next_generation(self, population, treshold, time_treshold, averages=[], bestOne=None, i=None):
        """
            input: - treshold = desired minimum fitness
                   - time_treshold = [start_time, amount of time you want to let it evolve]
                   - crossovers = rate in percent (0 ... 1.0)
                   - mutation = rate in percent (0 ... 1.0)
        """
        if time_treshold != None:
            if (time_treshold[0] + time_treshold[1]) <= time.time():
                print("******TERMINATED******")
                _max = max([self.fitness(i) for i in population])
                peak = [a for a in population if self.fitness(a) == _max][0]
                self.peak = peak
                self.writeFile(averages)
                
                return None

    
        bests = 0.5 # for keeping the best
        toBeKept = self.keepBest(list(population), int(len(population) * bests))

        selected = self.selectIndividuals(population)

        #breed the new population
        next_pop = self.breed(selected, 1)

        if averages != []:
            print(averages[len(averages) - 1])
        
        l = ([self.fitness(i) for i in population])
        peak = max(l)
        _best = [a for a in population if self.fitness(a) == peak][0]
        if self.reversedFitness(peak) <= int(treshold):
            self.peak = _best
            self.writeFile(averages)
            return None
        
        averages.append(self.reversedFitness(peak))

        #exchange individual if it is better than its ancestor
        for i in range(int(bests * self.population_size)):
            j = random.randint(0, self.population_size - 1)
            if self.fitness(next_pop[j]) <= self.fitness(toBeKept[i]):
                next_pop[j] = toBeKept[i]

        self.next_generation(next_pop, treshold, time_treshold, averages)  

    def check(self, triangles, pop):
        for p in pop:
            try:
                raw = []
                for seq in p:
                    for s in seq:
                        raw.append([s[0], s[1], s[2]])

                for t in triangles:
                    v = [t[0], t[1], t[2]]
                    raw.remove(v)
            except:
                print("Wrong triangles")
                print(p)
                exit()

    def fitness(self, basepairs):
        bs = basepairs
        bs = [a for a in bs if a != []]
        f = hm.fitness(bs)
        f += self.add
        for seq in bs:
            a_sum = sum([s[0] for s in seq])
            if a_sum > 180:
                return 0.00001

        return (100000/f) ** 10

    def reversedFitness(self, number):
        root = number ** (10**-1)
        return int(100000 / root)

    def generateSequences(self, size, triangles):
        for _ in range(size):
            random.shuffle(triangles)
            yield FindBestSequence(triangles).finalSequence

    def switchSequences(self, pop, activation):
        for p in pop:
            r = random.randint(0, 100)
            if r <= int(activation * 100):
                random.shuffle(p)
        return pop

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def keepBest(self, population, number):
        """
            number: number of individuals to keep
        """
        toBeKept = []
        for _ in range(number):
            _max = max([self.fitness(i) for i in population])
            peak = [a for a in population if self.fitness(a) == _max][0]

            toBeKept.append(peak)
            population.remove(peak)

        return toBeKept


    def writeFile(self, averages):
        f = open("averages.txt", "w")
        for a in averages:
            f.write(str(a) + "\n")
        f.close()

    def breed(self, population, crossovers):
        new_pop = [] # the next generation

        for _ in range(int(len(population))): #because each parent will get one child
            a = random.choice(population)
            b = random.choice(population)    
            child = None
            if self.fitness(a) > self.fitness(b):       
                child = Breeding(a, b, random.randint(0, len(a) - 1)).child()
            else:
                child = Breeding(b, a, random.randint(0, len(a) - 1)).child()
            new_pop.append(child)
            
        return new_pop

    
        
    def selectIndividuals(self, population):
        total_fitness = sum([self.fitness(ind) for ind in population])
        weights = [self.fitness(p)/total_fitness for p in population]
        choices = list(np.random.choice(len(population), len(population), p=weights))
        
        new_pop = []

        for c in choices:
            new_pop.append(population[c])

        return new_pop