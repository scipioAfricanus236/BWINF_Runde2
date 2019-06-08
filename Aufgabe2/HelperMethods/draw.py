
#draw.py class Draw:
#Draw uses svgwrite to create a .svg file with the visualized output


import svgwrite

class Draw:
    #in this variant the origin is not needed
    def __init__(self, polygones, filename):
        #polygones = the obstacles in Lisa's way,
        #origin = Lisa's house
        self.polygones = polygones
        #self.origin = origin
        self.filename = filename
        self.drawing = svgwrite.Drawing(filename=self.filename, profile='full')
        if polygones != None:
            self.draw()

    def draw(self):
        drawing = self.drawing

        #these aer her obstacles
        for polygon in self.polygones:
            drawing.add(drawing.polygon(polygon, fill="#8B8682"))

        #this is Lisa's home
        #drawing.add(drawing.circle(center=self.origin, r=15, fill="red"))

        #this is the bus road
        drawing.add(drawing.line([0, 0], [0, 10000000], stroke="gray", stroke_width="20"))

        drawing.save()

    def edges(self, edges):
        #this function adds the edges that were specified in the input to the .svg file
        edges = self.moveByVector(edges, [10,100])
        for i in edges:
            self.drawing.add(self.drawing.line(i[0], i[1], stroke="black", stroke_width="4"))
        self.drawing.save()

    def moveByVector(self, edges, vector):
        for edge in edges:
            for p in edge:
                p[0] += vector[0]
                p[1] += vector[1]
        return edges

