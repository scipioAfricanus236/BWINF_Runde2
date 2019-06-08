from findIntersection import FindIntersection
from sequenceToEdges import SequenceToEdges as se
import time


class MoveTogether:
    """This class accepts a list of a sequence of edges as input and moves these edges together"""

    def __init__(self, edges):
        self.edges = edges

    @property
    def transformed_edges(self):
        return self.reduceToOneList(self.final_sequence)

    
    def moveTogether(self):
        edges_sequence = self.edges
        final = [edges_sequence[0]]

        for i in range(len(edges_sequence) - 1):
            self.moveEdges_sequence(final[len(final) - 1], edges_sequence[i + 1], [0,0])

            final.append(self.sequence)
            self.sequence = None

        self.final_sequence = final

    def moveEdges_sequence(self, prior, sequence, vector):
        iteration = 0.1
        sequence = self.moveEdges(sequence, vector)
        together = sequence + prior

        if self.findIntersection(together) == False:
            vector[0] -= iteration
            self.moveEdges_sequence(prior, sequence, vector)
        else:
            sequence = self.moveEdges(sequence, [6,0])
            self.sequence = sequence

    def findIntersection(self, edges_sequence):
        find = FindIntersection(edges_sequence, 1)

        for edge in edges_sequence:
            if find.isItPossible(edge):
                return True
        return False

    def reduceToOneList(self, coordiantes):
        """This function reduces the enormous list of all sequences with all triangles to one 
        bigger list with all coordinates of all placed triangles"""
        new = []
        for c in coordiantes:
            for b in c:
                new.append(b)
        return new
    
    def moveEdges(self, edges, vector):
        for edge in edges:
            for point in edge:
                point[0] = round(point[0] + vector[0], 1)
                point[1] = round(point[1] + vector[1], 1)

        return edges