import sys 
sys.path.append("/Users/juliuside/Desktop/BWINF_Runde2/Aufgabe2/HelperMethods/")

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import logging
from collections import namedtuple
import itertools
import random

import GeneticAlgorithm as ga
from findBestSequence import FindBestSequence
import HelperMethods as hm
from knapsack import Knapsack

class Main:
    def __init__(self, filename):
        self.filename = filename

        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename = "henning.log", level = logging.DEBUG, format = LOG_FORMAT, filemode="w")
        logger = logging.getLogger()
        logger.info("beginning")

        triangles = hm.textToTriangles(self.filename)
        self.triangles = list(triangles)
        logger.info("calculating the triangles")
        sequences = None
        
        if sum([t[0] for t in triangles]) <= 180:
            sequences = []
            sequences.append(list(triangles))
        else:
            result = self.head(triangles)
            head = result[0]
            triangles = result[1]
            result = self.head(triangles)
            tail = result[0]
            triangles = result[1]

            if sum([t[0] for t in triangles]) <=  180:
                if triangles != []:
                    sequences = [head, triangles , tail]
                else:
                    sequences = [head, tail]
            else:
                pop_size = 20
                sec = 5
                sequences = self.rest(list(triangles))
                sequences.insert(0, head)
                sequences.append(tail)
                sequences = self.run(triangles, pop_size, sec, head, tail)
        #self.plotFile()
        self.drawSequences(sequences)

        print("input filename: ", self.filename)
        print("Total distance: ", self.distance)
        print("Coordinates: ", self.coordinates)
        print("output filename: ", self.filename.replace("txt", "svg"))

    
    def head(self, triangles):
        LIMIT = 180
        knapsack = Knapsack(triangles, LIMIT)
        head = knapsack.main()
        for h in head:
            triangles.remove(h)
        head = self.sortHead(head)
        return [head, triangles]
    
    def sortHead(self, triangles, reverse=True):
        lengths = [t[1] for t in triangles]
        lengths.sort(reverse=reverse)

        sorted = []
        for l in lengths:
            for t in triangles:
                if l == t[1]:
                    sorted.append(t)
                    triangles.remove(t)
                    break
        
        return sorted

    def rest(self, triangles):
        remainig = []
        while True:
            ks = Knapsack(triangles, 180)
            seq = ks.main()
            for s in seq:
                triangles.remove(s)
            remainig.append(seq)
            if triangles == []:
                break

        return remainig


    def run(self, triangles, pop_size, sec, head, tail):
        add = hm.completeFitness([head, tail]) #hm.sequenceToEdges([self.head, self.tail])[1]
        print(add, "here")
        sequences = ga.optimization(triangles, pop_size, 700.0, sec, add)

        for s in sequences:
            s = self.sortSequence(s)

        sequences.insert(0, head)
        sequences.append(tail)

        return sequences


    def drawSequences(self, sequences):
        fitness = hm.completeFitness(sequences)

        #finding out the ids of the triangles
        _raw = [s for seq in sequences for s in seq]
        tris = list(self.triangles)
        ids = [self.triangles.index(r) + 1 for r in _raw]        
        self.ids = ids

        peak = hm.sequenceToEdges(sequences)
        edges = []
        #moved together
        _edges = hm.moveTogether(peak[0]) 

        if _edges[1] < 0:
            fitness += _edges[1]
            edges = _edges[0]
        else:
            edges = []
            for a in peak[0]:
                for b in a:
                    edges.append(b)

        tris = [edges[i*3:i*3+3] for i in range(int(len(edges) / 3))]
        self.coordinates = [set([tuple(point) for edge in t for point in edge]) for t in tris]

        self.distance = fitness
        hm.save(edges, fitness, "peak.txt")
        
        hm.draw(edges, 0.9, self.filename.replace("txt", "svg"))
        #self.plotFile()

    def plotFile(self, file="averages.txt"):
        file = open(file, "r")

        y = [line for line in file]
        x = [i for i in range(len(y))]

        plt.plot(x, y, color='g')
        plt.plot(x, [y[len(y) - 1]] * len(y), color='orange')
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.show()

    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #the following function will straighten up all the edges, so that the longest edges stick to the top

    def sortSequence(self, sequence):
        """input: sequence as Triangles """
        sorted_triangles = self.indexTriangles(sequence)
        transformed = [None] * len(sorted_triangles)
        peak = int((len(sequence) / 2))

        iterator = True
        leftside = 1
        rightside = 1
        transformed[peak] = sorted_triangles[0]
        sorted_triangles.pop(len(sorted_triangles) - 1)

        for triangle in sorted_triangles:
            if iterator == True:
                transformed[peak - leftside] = triangle
                leftside += 1
                iterator = False
            else:
                transformed[peak + rightside] = triangle
                rightside += 1
                iterator = True

        return transformed         

    def indexTriangles(self, triangles):
        largest_lengths = [t[1] for t in triangles]
        largest_lengths.sort(reverse = True)
        sorted_triangles = []

        for a in largest_lengths:
            for b in triangles:
                if a == b[1]:
                    sorted_triangles.append(b)
                    break

        return sorted_triangles




test = Main("/Users/juliuside/Desktop/BWINF_Runde2/Aufgabe2/examples/dreiecke5.txt")

