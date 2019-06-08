
#findIntersection.py class FindIntersection
#   -this class is meant to check if a possible path to the bus intersects with any obstacles

#   -it can check that if it receives a list of lines in [[x1, y1], [x2, y2]] format as an input

#   -these lines should be the borders of Lisa's obstacles (the polygones)


class FindIntersection:
    def __init__(self, lines):
        #because the lines / obstacles do not change we can store it like this
        self.lines = lines

    def isItPossible(self, road):
        #lines = all the lines 
        #road = the two points where Lisa would like to walk
        #this function checks if a road does not cross any line

        for line in self.lines:
            if (line != road and line[0] != road[1] and line[0] != road[0]):  
                if self.findIntersection(line, road):
                    return True
            
        return False

    def findIntersection(self, a, b):
        #this function will determine if two lines cross
        #the format should be (x, y)
        #it returns true if two lines intersect

        functionA = self.__functionExpression__(a)
        functionB = self.__functionExpression__(b)

        if functionA == None or functionB == None:
            return None

        if functionA[0] == functionB[0]:
            return False

        #if two lines have a common point, they do not intersect
        if a[0] == b[0] or a[0] == b[1] or a[1] == b[0] or a[1] == b[1]:
            return False

        if len(functionA) == 2:
            if len(functionB) == 2:
                x = (functionB[1] - functionA[1]) / (functionA[0] - functionB[0])
                if x >= a[0][0] and x <= a[1][0] and x >= b[0][0] and x <= b[1][0]:
                    return True
                else:
                    return False
            else:
                return self.__infinitySlope__(functionB[0], b, functionA, a)
        else:
            if len(functionB) == 2:
                return self.__infinitySlope__(functionA[0], a, functionB, b)
            else:
                return False
                

    def __infinitySlope__(self, x, a, function, b):
        #this function finds out if two lines interdect when one line goes vertically
        #a has infinity slope (x)
        #b can be represented by a normal function
        #input: 
        #       x as a constant,
        #       a as a line (x1, y1) and (x2, y2),
        #       function as a normal function (mx +c)(__functionExpression)

        # x = c for function a
        y = function[0] * x + function[1]
        
        if y > a[0][1] and y < a[1][1] or y > a[1][1] and y < a[0][1]:
            if x > b[0][0] and x < b[1][0] or x > b[1][0] and x < b[0][0]:
                return True
        else: 
            return False


    def __functionExpression__(self, line):
        #this functions returns a function expression
        #input = (x1, y1) and (x2, y2)
        #output = mx + c as a list [m, c]

        if line[1][0] < line[0][0]:
            l = line[1]
            line[1] = line[0]
            line[0] = l
        
        if line[1][0] == line[0][0]:
            return [line[0][0]]

        m = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
        c = line[1][1] - m * line[1][0]

        return [m, c]
