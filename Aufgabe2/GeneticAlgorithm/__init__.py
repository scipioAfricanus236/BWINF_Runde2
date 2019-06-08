""" 
        This package accepts an input (a list of triangles) and returns the best overall sequence, 
        ergo, a list of sequences of triangles indicated by the smallest angle and the largest edge is returned.
"""
import sys 
sys.path.append("/Users/juliuside/Desktop/BWINF_Runde2/Aufgabe2/GeneticAlgorithm")
from population import Population
import csv

def optimization(triangles, pop_size, treshold, time, add):
    invalid_elements = [i for i in triangles if len(i) != 3]

    if invalid_elements:
        raise ValueError("Wrong input, every elements has to have the value of the smallest angle and the largest edge")

    pop = Population(triangles, pop_size, treshold, time, add)
    indi = pop.optimizedIndividual
    if indi == None:
        return None
    else:
        bs = indi
        bs = [a for a in bs if a != []]
        return bs
    


