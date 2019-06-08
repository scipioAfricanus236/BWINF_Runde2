from textToPolygones import TextToPolygones
from findIntersection import FindIntersection
from draw import Draw
from graph import Edge, Graph
from finalPath import FinalPath

from itertools import combinations
import numpy as np

import sys
import logging

class LisasRoute:
    def __init__(self, filename=None):
        if filename == None:
            filename = input("Please enter the filename:")
        self.filename = filename
        self.polygones = TextToPolygones(filename).getData()["polygones"]
        self.origin = TextToPolygones(filename).getData()["origin"]
        self.main()


    def main(self):
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename = "henning.log", level = logging.DEBUG, format = LOG_FORMAT, filemode="w")
        logger = logging.getLogger()
        logger.info("beginning")
        
        points = self.getRawPoints(self.polygones, self.origin)
        self.possibleEdges = list(combinations((points), 2))
        logger.info("possible edges")

        finalEdges = self.addIntersectionWithTheBus(points)
        logger.info("intersections with the bus")

        edges = self.getPossibleLines(points, self.polygones, self.possibleEdges)
        logger.info("final edges")

        edges = self.eliminateInnerEdges(self.polygones, edges)
        logger.info("eliminate inner edges")

        allEdges = finalEdges + edges
        self.graph = Graph((self.getEdges(allEdges)))
        logger.info("graph is created")
        
        path = FinalPath(finalEdges, self.graph, self.origin)
        logger.info("get final path")
        
        self.draw(path.edges)

        print("Distance to the bus (in m): ", path.distance)
        print("Required time for Lisa to reach the bus (in s): ", path.time)
        print("Departure: ", path.departure)
        print("Arrival at the bus :", path.arrival)
        print("Distance the bus has already driven when Lisa enters the bus (in m):", path.arrivalinM)
        print("Path:", path.path)
        self.path = path
        print("Polygones:", self.polygones)

    def draw(self, edges):
        # this function adds the edges to the graphical output
        drawing = Draw(self.polygones, self.origin,
                       self.filename.replace("txt", "svg"))
        drawing.edges(edges)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # MARK :- the head functions

    def getEdges(self, allEdges):
        # this function returns the edges in a Edge(start, end, cost) format
        edges = []
        for e in allEdges:
            x = (abs(int(e[1][0]) - int(e[0][0]))) ^ 2
            y = (abs(int(e[1][1]) - int(e[0][1]))) ^ 2
            length = np.sqrt(x + y)

            edges.append(self.__makeEdge__(tuple(e[0]), tuple(e[1]), length))
            edges.append(self.__makeEdge__(tuple(e[1]), tuple(e[0]), length))
        return edges

    def __makeEdge__(self, start, end, cost):
        return Edge(start, end, cost)

    def getPossibleLines(self, points, polygones, possibleEdges):
        # this function returns all the possible edges where Lisa could effeciently walk
        lines = []

        for p in polygones:
            lines.append(self.polygonToLines(p))

        lines = self.reduceToOneList(lines)
        find = FindIntersection(lines)
        # a big list with all edges of polygones if created

        trueEdges = []
        # this section checks for every possible edge if it intersects with any other edge of any polygones
        for edge in possibleEdges:
            if find.isItPossible(list(edge)) == False:
                trueEdges.append(edge)

        # all the free paths where Lisa could walk from polygon to polygon are returned
        return trueEdges

    def eliminateInnerEdges(self, polygones, edges):
        # this function gets rid of lines within a polygon
        # they arent detetected by the algorithm because it does not intersect with any other polygones
        # input: polygones, edges as lists

        trueEdges = []
        used = [None] * 4  # this keeps track to what polygones the edges belong
        # for the first edge:    used[0] = number of polygones
        #                        used[1] = number of point
        # for the second edge:   used[2] = number of polygones
        #                        used[3] = number of point

        for edge in edges:
            if edge[0] == self.origin or edge[1] == self.origin:
                trueEdges.append(edge)
            else:
                for i in range(len(polygones)):
                    # iterates through every polygon
                    for j in range(len(polygones[i])):
                        # iterates through every point of a certain polygon
                        if edge[0] == polygones[i][j]:
                            used[0] = i
                            used[1] = j
                        if edge[1] == polygones[i][j]:
                            used[2] = i
                            used[3] = j

                if used[0] == used[2]:
                    polygon = polygones[used[0]]
                    priorNode = polygon[(used[3] - 1) % len(polygon)]
                    nextNode = polygon[(used[3] + 1) % len(polygon)]

                    if edge[0] == priorNode or edge[0] == nextNode:
                        # means it is not a diagonal
                        trueEdges.append(edge)
                else:
                    trueEdges.append(edge)

        return trueEdges

    def unique(self, edges):
        # this function makes sure that the edges are unique
        # e.g. [3, 5], [6, 8] and [6, 8], [3, 5] are the same two lines

        true_edges = []
        skip = False

        for e in edges:
            for t in true_edges:
                if e[0] == t[1] and e[1] == t[0]:
                    skip = True
            if skip == False:
                true_edges.append(e)
            skip = False
        return true_edges

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # MARK :- Helper methods

    def getRawPoints(self, polygones, origin):
        new = []

        for a in polygones:
            for b in a:
                new.append(b)
        new.append(origin)
        return new

    def findIntersection(self, polygones, road):
        lines = []

        for p in polygones:
            lines.append(self.polygonToLines(p))

        lines = self.reduceToOneList(lines)
        find = FindIntersection(lines)

        return find.isItPossible(road)

    def reduceToOneList(self, polygones):
        # this function breaks the huge list of lines of different polygones down into one list of lines
        # input: polygones as a multidimensional list of lines
        lines = []
        for p in polygones:
            for i in p:
                lines.append(i)

        return lines

    def polygonToLines(self, polygon):
        # this function returns all the lines of one polygon

        lines = []
        for i in range(len(polygon)):
            lines.append([polygon[i], polygon[(i + 1) % len(polygon)]])
        return lines

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # MARK:- this section looks for a possible direct way to the road for every point

    def addIntersectionWithTheBus(self, points):
        newEdges = []
        for p in points:
            alpha = self.__getAlpha__(p)
            line = self.__findLine__(alpha, p)

            if self.findIntersection(self.polygones, line) == False:
                newEdges.append(line)
            else:
                alternativeLine = self.__findNearestSpot__(p)
                if alternativeLine != None:
                    newEdges.append(alternativeLine)
        return newEdges

    def __findNearestSpot__(self, origin):
        optimum = self.__getAlpha__(origin)
        validValues = []
        alphas = []

        for a in range(90):
            line = self.__findLine__(a, origin)
            if self.findIntersection(self.polygones, line) == False:
                validValues.append(abs(optimum - a))
                alphas.append(a)

        if (validValues != []):
            minimum = min(validValues)
            index = validValues.index(minimum)
            bestFit = alphas[index]

            return self.__findLine__(bestFit, origin)
        else:
            return None

    def __getAlpha__(self, point):
        # returns the best angle of starting running
        # bus: 30 km/h
        # lisa: 15 km/h
        # convert from meters to kilometers
        x = point[0]/1000 #form point
        y = point[1]/1000

        def left(x, y, a): return (y + np.tan(np.deg2rad(a)) * x) / 30
        def right(x, a): return x/np.cos(np.deg2rad(a)) / 15


        max = [None, None]

        for a in range(90):
            #value = left(x, y, a) - right(x, a)
            value = np.tan(np.deg2rad(a)) - 2 / np.cos(np.deg2rad(a)) - y/x
            
            if (max[0] == None or value > max[0]):
                max[0] = value
                max[1] = a
        
        
        return max[1]

    def __findLine__(self, angle, origin):
        # this function creates a lines between an input origin and the y-axis at a given angle
        # the format is [x1, y1], [x2, y2]
        line = []
        # first point origin
        line.append(origin)
        # second point intersection with y-axis
        line.append([0, origin[0] / np.cos(np.deg2rad(angle)) * np.sin(np.deg2rad(angle)) + origin[1]])

        return line

