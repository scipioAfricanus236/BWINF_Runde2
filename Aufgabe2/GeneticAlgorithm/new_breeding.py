from findBestSequence import FindBestSequence
import random


import sys 
sys.path.append("/Users/juliuside/Desktop/BWINF_Runde2/Aufgabe2")
import HelperMethods as hm


class Breeding:
    def __init__(self, a, b, num_of_seq):
        """
            a has the better fitness
        """
        self.a = a
        self.b = b
        self.num_of_seq = num_of_seq

    def child(self):
        best_a = self.findBestNseqs(list(self.a), self.num_of_seq)
        new = self.bred(self.a, self.b, best_a)
       
        return new


    def bred(self, a, b, seqs):
        """
            a has the better sequence (seq)
        """ 
        indexe = [a.index(s) for s in seqs]
        remaining = self.removeSequences(list(a), seqs)

        new = self.bestRemaining(remaining, 10)

        for i, index in enumerate(indexe):
            new.insert(index, seqs[i])

        return new

    def bestRemaining(self, remaining, times):
        min = [None, None]
        for _ in range(times):
            random.shuffle(remaining)
            new = FindBestSequence(remaining).finalSequence
            v = hm.fitness(new)

            if min[0] == None or v <= min[0]:
                min[0] = v
                min[1] = new
            
        return min[1]


    def removeSequences(self, a, seqs):
        """
            - finds the remaining triangles so new sequences can be formed
            - several sequences can be deleted
        """
        
        all = [s for seq in a for s in seq]
        for seq in seqs:
            for s in seq:
                all.remove(s)
        return all



    def findBestNseqs(self, a, n):
        """
            input: - a: (list of named tuple) triangles
                   - n: (int) number of desired sequences to stay in the next individual
        """
        seqs = []
        for _ in range(n):
            seq = self.findBestSeq(a)
            seqs.append(seq)
            a.remove(seq)
        
        return seqs



    def findBestSeq(self, a):
        min = None
        index = 0

        for i, seq in  enumerate(a):
            v = self.sequenceFitness(seq)

            if min == None or v <= min:
                min = v
                index = i

        return a[index]


    def sequenceFitness(self, seq):
        if seq == []:
            return 0
        l = [f[1] for f in seq]
        lf = 0
        lf = self.__lengths_fitness__(l) * 10
        lf += seq[0][2][1] 
        lf += seq[len(seq) - 1][2][0] 
        return lf ** 5


    def __lengths_fitness__(self, lengths):
        """ This function to determine how well the lengths are distributed in order to be able to calculate the fitness
            of all the lengths. 
            In the ideal case the slopes between the lengths on the left side equal the ones on the right side
            with the largest length in the middle. (Gaussian Distribution)
            Then it returns the difference between the sums of the left and right side.
        """

        peak = int(len(lengths) / 2)

        left = []
        right = []

        for i, l in enumerate(lengths):
            if i < peak:
                left.append(l)
            if i > peak:
                right.append(l)
        
        left_slopes = self.__calculate_slopes__(left)
        right_slopes = self.__calculate_slopes__(right)

        left = abs(sum(left_slopes))
        right = sum(right_slopes)

        return (left - right)

    def __calculate_slopes__(self, lengths):
        """This function calculates all the slopes between the largest lengths of the triangles of a sequence.
            The idea behind this is that if a sequence has triangles with varying lengths it will take less space.

            input: lengths = a list of lengths as integers
         """
        
        for i in range(len(lengths) - 1):
            rate = lengths[i + 1] / lengths[i]

            if rate < 1:
                #goes down
                yield -(lengths[i] / lengths[i + 1])
            else:
                yield rate