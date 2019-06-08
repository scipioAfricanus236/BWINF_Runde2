import sys 
sys.path.append("/Users/juliuside/Desktop/bwinfRound2/Aufgabe2/GeneticAlgorithm/")

from breeding import Breeding
from DNA import DNA

import unittest

class BreedingTestCase(unittest.TestCase):
    def setUp(self):
        #self.b = DNA([[[1,2], [3,4], [5, 6]]])
        #self.a = DNA([[[5, 6], [3, 4], [1, 2]]])
        pass

    def test_updateResult(self):
        up = Breeding.__updateResult__
        self.assertListEqual(up(None, [1, 2, 3], [1, 2, 3]), [1, 2, 3])
        self.assertListEqual(up(None, [5, 5, 6, 7], [5, 6, 6, 7]), [5, 5, 6, 7])
        self.assertRaises(TypeError, up, (None, [1.0, 2, 3], [1, 2, 3]))

        a = [0, 1, 31, 3, 5, 5, 21, 35, 12, 9, 9, 11, 10, 28, 14, 15, 23, 17, 14, 19, 18, 21, 17, 3, 6, 22, 22, 20, 4, 29, 30, 31, 32, 23, 35, 11, 7]
        tris = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
        result = up(None, a, tris)

        for t in tris:
            result.remove(t)
    
    def test_crossover(self):
        co = Breeding.crossover 
        #print(co(None, [[1,2], [3,4], [5, 6]], [[5, 6], [3,4], [1,2]] , 30), "crossover")

    def test_rebuildSequences(self):
        rs = Breeding.__rebuildSequences__
        a = [1, 2, 3]
        lengths = [1, 1, 1]
        result = rs(None, a, lengths)    
        self.assertListEqual(result, [[1], [2], [3]])
        a = [1, 2, 4, 5, 6, 7, 8]
        lengths = [1]
        self.assertRaises(ValueError, rs, None, a, lengths)
        lengths = [3, 2, 2]
        self.assertListEqual(rs(None, a, lengths), [[1, 2, 4], [5, 6], [7, 8]])

    def test_init(self):
        breeding = Breeding([1,2,3], [3, 2, 1], [2,1], 2)
        self.assertListEqual(breeding.id_list, [3,2,1])

    def test_breed(self):
        breeding = Breeding([1, 2, 3], [3, 2, 1], [2, 1], 2)
        print(breeding.breed, "breed")


if __name__ == "__main__":
    unittest.main()