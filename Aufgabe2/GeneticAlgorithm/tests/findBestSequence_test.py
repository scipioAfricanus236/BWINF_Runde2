import sys 
sys.path.append("/Users/juliuside/Desktop/bwinfRound2/Aufgabe2/GeneticAlgorithm/")

from findBestSequence import FindBestSequence
import unittest

class FindBestSequenceTestCase(unittest.TestCase):
    def test_subsetSum(self):
        triangles = [[[60], [1], [1, 2]], [[60], [1], [1, 2]], [[60], [1], [1, 2]]]
        find = FindBestSequence([0])

        result = next(find.subset_sum(triangles, 180))
        print(result)


if __name__ == "__main__":
    unittest.main()