import numpy as np
class FinalPath():
    """
        This class finds the best path for Lisa.
        It takes a graph, the origin and the edges that intersect with the y-axis
        and finds the path that lets her leave her house as late as possible.
    """

    def __init__(self, finalEdges, graph, origin):
        self.graph = graph
        self.origin = origin
        self.finalEdges = finalEdges
        self.shortestPath = self.__findShortestPath__()

    def __findShortestPath__(self):
        minimum = [None, None]

        for path in self.__pathToFinalEdges__(self.finalEdges):
            time = self.timeForAPath(path)

            if (minimum[0] == None or time >= minimum[0]):
                minimum[0] = time
                minimum[1] = path
        minimum[0] = self.__lengthOfAPath__(minimum[1])
        return (minimum)
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @property
    def path(self):
        return list(self.shortestPath[1])

    @property
    def edges(self):
        return self.pointsToEdges(self.shortestPath[1])

    @property
    def distance(self):
        return self.shortestPath[0]
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def time(self):
        #returns the required time for Lisa to reach the bus if she constantly runs 15 km/h
        lisasVelocity = 15 #km/h
        mPS = lisasVelocity / 3.6 #meter per second
        requiredTime = self.shortestPath[0] / mPS
        
        return requiredTime  

    def timeForAPath(self, path):
        self.shortestPath = [self.__lengthOfAPath__(path), path]
        return self.departure

    @property
    def arrivalinM(self):
        return self.__whenLisaEntersTheBus__(self.shortestPath[1]) * 30/3.6

    @property
    def arrival(self):
        time = self.__whenLisaEntersTheBus__(self.shortestPath[1])
        return self.__secToTime__(7*3600 + 30*60 + time)

    @property
    def departure(self):
        #returns the latest possible departure as a string, e.g '07:15:58'        
        time = self.__whenLisaEntersTheBus__(self.shortestPath[1])
        busDeparture = 7*3600 + 30*60 + time #the bus' departure in seconds
        difference = busDeparture - self.time

        return self.__secToTime__(difference)
    
    def __whenLisaEntersTheBus__(self, path):
        shortestPath = list(path)
        whenLisaEntersTheBus = shortestPath[len(shortestPath) - 1][1]

        velocityOfTheBus = 30 / 3.6 #in meters per seconds
        time = whenLisaEntersTheBus/velocityOfTheBus

        return time

    def __secToTime__(self, seconds):
        hours = int(seconds / 3600)
        seconds -= hours * 3600
        if hours < 10:
            hours = "0" + str(hours)

        min = int(seconds / 60)
        seconds -= min * 60
        if min < 10:
            min = "0" + str(min)

        seconds = int(seconds)
        if seconds < 10:
            seconds = "0" + str(seconds)

        time = (str(hours) + ":" + str(min) + ":" + str(seconds)) 

        return time

    def __pathToFinalEdges__(self, finalEdges):
        paths = []
        
        for edge in finalEdges:
            if edge[0][0] == 0:
                paths.append(self.graph.dijkstra(self.origin, edge[0]))
            elif edge[1][0] == 0:
                paths.append(self.graph.dijkstra(self.origin, edge[1]))
            else:
                raise ValueError("Final edges have to intersect with the y-axis: {}".format(edge))

        return paths        

    def __lengthOfAPath__(self, path):
        distance = 0

        for i in range(len(path) - 1):
            #(y2 - y1)^2 + (x2 - x1)^2 = edge
            length = lambda a: (path[(i + 1) % len(path)][a] - path[i][a])
            # length(0) = x, length(1) = y
            distance += np.sqrt(np.power(int(length(0)), 2) + np.power(int(length(1)), 2))

        return distance
    
    def pointsToEdges(self, path):
        edges = []
        for i in range(len(path)):
            if i != (len(path) - 1):
                edges.append([path[i], path[(i + 1) % len(path)]])
        
        return edges
