import sys 
sys.path.append("/Users/juliuside/Desktop/bwinfRound2/Aufgabe2/GeneticAlgorithm/")

import unittest

from fitness import Fitness
from DNA import DNA

class FitnessTestCase(unittest.TestCase):
    def test(self):
        seq = [[[16, 94], [41, 75], [25, 116], [29, 91], [28, 78], [35, 75]], [[22, 53], [32, 116], [43, 106]], [[38, 105], [37, 43], [18, 109], [12, 82], [50, 75]], [[6, 120], [54, 70], [32, 98], [50, 97], [26, 80]], [[13, 105], [30, 112], [31, 100]], [[23, 71], [32, 89], [29, 91], [22, 59]], [[38, 91], [38, 98], [11, 203], [24, 105], [25, 111], [54, 78], [44, 85], [49, 82], [58, 72], [30, 86], [22, 112]]]
        f = Fitness(DNA(seq))
        print(f.fitness)


if __name__ == "__main__":
    unittest.main()