import numpy as np
from polygonesToAngle import Triangle
from findIntersection import FindIntersection

class SequenceToEdges:
    def __init__(self, triangles):
        """
            -input: - triangles: (Triangle(smallest angle, largestEdge, edges))
        """
        # a sequence is all the triangles around a common point
        self.sequences = triangles

    @property
    def fitness(self):
        """
            returns the total distance of a sequence
        """

        co = self.coordinates
        first = co[0][0][2][0]
        last = co[len(co) - 1][0][2][0]
        # edges = self.edges
        # first = edges[2][1][0]
        return abs(last - first)

    @property
    def middleFitness(self):
        co = self.coordinates
        first =  self.extremeXCoordinates(co[0])[0]
        last = self.extremeXCoordinates(co[len(co) - 1])[1]
        return abs(last - first)

    @property
    def coordinates(self):
        """

        """
        coordinates = []
        x = 100

        for i, s in enumerate(self.sequences):
            if i == 0:
                sequence = self.convertTrianglesToCoordinates(s)
                for s in sequence:
                    for p in s:
                        p[0] *= -1
                
            else:
                sequence = self.convertTrianglesToCoordinates(s)

            extremeX = self.extremeXCoordinates(sequence)
            x += extremeX[0]
            moved = self.move(sequence, [x, 0])
            x += extremeX[1]
            coordinates.append(moved)

        return coordinates
    
    @property
    def edges(self):
        return self.coordiantesToEdges()

    def coordiantesToEdges(self):
        """This function converts the initial coordinates into a list of sequences of a list of edges.
            All the edges of one sequence (around a common point with the road) are stored together.

            - e.g. [[edge1, edge2, edge3], [edge1, edge2, edge3]] 
                            sequence1           sequence2
         """

        edges_sequence = []

        for sequence in self.coordinates:
            edges_list = []
            for edges in sequence:
                edges_list.append(self.polygonToLines(edges))
            edges_sequence.append(self.reduceToOneList(edges_list))
        return edges_sequence
    

    def polygonToLines(self, polygon):
        # this function returns all the lines of one polygon

        lines = []
        for i in range(len(polygon)):
            lines.append([polygon[i], polygon[(i + 1) % len(polygon)]])
        return lines

    def extremeXCoordinates(self, sequence):
        """This function returns the smallest and biggest x coordinate of a given sequence"""
        min = None
        max = None

        for s in sequence:
            for point in s:
                if (min == None or point[0] < min):
                    min = point[0] #the smallest x coordinate
                if (max == None or point[0] > max):
                    max = point[0] #the biggest x coordinate

        return [abs(min), abs(max)]

    def move(self, triangles, vector):
        """
            This function moves a certain amount of triangles by a given vector
        """
        for triangle in triangles:
            for point in triangle:
                point[0] += vector[0]
                point[1] += vector[1] 
        return triangles

    def reduceToOneList(self, coordiantes):
        """This function reduces the enormous list of all sequences with all triangles to one 
        bigger list with all coordinates of all placed triangles"""
        new = []
        for c in coordiantes:
            for b in c:
                new.append(b)
        return new

    def convertTrianglesToCoordinates(self, triangles):
        """
            This function converts a sequence of triangles into coordiantes.
        
            input: triangles = [Triangle(smallestEdge: 10, largest_edge:45.3, edges:10, 35), ...]
        """
        coordinates = []
        angle = 0

        for t in triangles:
            triangle = []

            for edge in t[2]:
                x = edge * np.cos(np.deg2rad(angle))
                y = edge * np.sin(np.deg2rad(angle))

                triangle.append([int(x), int(y)])
                angle += t[0]

            #the second triangle begins with the same angle the first one ends
            angle -= t[0] 

            triangle.append([0, 0])
            coordinates.append(triangle)

        return coordinates
   