#aufgabe 2 version

class TextToPolygones:
    def __init__(self, filename):
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        #getting rid of the information about the number of objects
        content.pop(0) 

        #self.origin = self.stringToInt(content[len(content) - 1]) #origin = Lisa's house
        #content.pop(len(content) - 1)
        self.main(content)

    def main(self, polygonesAsString):
        self.polygones = []
        for p in polygonesAsString:
            self.polygones.append(self.stringToPolygon(p))

    
    def getData(self):
        #return {"polygones": self.polygones, "origin": self.origin}
        return self.polygones

    def stringToInt(self, string):
        #this function converts a tring into a series of ints
        new = [[]]

        for s in string:
            if s != " ":
                new[len(new) - 1].append(s)
            else:
                new.append([])
        
        integers = []
        for n in new:
            integers.append(int("".join(n)))

        return integers

    def stringToPolygon(self, content):
        #this function converts a string into a list of points

        #maybe I should merge this function and stringToInt

        content = list(content)        
        new = [[]] 
        start = True

        for c in content:
            if start:
                if c == " ":
                    start = False 
                    #so that the number of polygones will not bother us 
            else:
                if c != " ":
                    new[len(new) - 1].append(c)
                else:
                    new.append([])

        x = True
        points = [[]]  

        for n in new:
            if x:
                points[len(points) - 1].append(int("".join(n)))
                x = False
            else:
                points[len(points) - 1].append(int("".join(n)))
                x = True
                points.append([])
               
        points.pop(len(points) - 1)

        return points

