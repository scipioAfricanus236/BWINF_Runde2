import numpy as np
from collections import namedtuple

Triangle = namedtuple("Triangle", "smallest_angle, largest_edge, edges")

class PolygonesToAngle:
    def __init__(self, polygones):
        self.polygones = polygones
        self.main()

    def main(self):
        """
        output:
            the output is a Triangle tuple

        !!!! first edge: left side, second edge: right side
        """
        
        triangles = []
        for polygon in self.polygones:
            edges = self.coordinatesToEdges(polygon)
            smallest_angle = min(self.calculateAngles(edges))
            largest_edge = max(edges)
            
            #remove the smallest edge
            #the smallest edge is the edge of the smallest angle, therefore, it wont be required to reassemble the triangles
            edges.remove(min(edges))
            
            triangles.append(Triangle(int(smallest_angle), int(largest_edge), edges))

        self.triangles = triangles

    def coordinatesToEdges(self, nodes):
        if len(nodes) != 3:
            raise ValueError("A triangle must  have exactly three edges")
  
        edges = []
        for i in range(len(nodes)):
            #(y2 - y1)^2 + (x2 - x1)^2 = edge
            length = lambda a: nodes[(i + 1) % len(nodes)][a] - nodes[i][a]
            edges.append(int(np.sqrt(np.power(length(0), 2) + np.power(length(1), 2))))
        return edges

    def calculateAngles(self, edges):
        #this function calculates the inner angles of the Triangle
        #by using the law of cosine    
        #a^2 = b^2 + c^2 -  2ab * cos(alpha)
        # -> alpha = acos()
        angles = []

        for i in range(len(edges)):
            dividend =  - edges[i]**2 + edges[(i + 1) % len(edges)]**2 + edges[(i - 1) % len(edges)]**2
            divisor = 2 * edges[(i + 1) % len(edges)] * edges[(i - 1) % len(edges)]
            #print(edges[i], "Dividend", dividend, "Divisor", divisor)
            angle = np.rad2deg(np.arccos(dividend / divisor))
            angles.append(round(angle))

        return angles
