class EdgesToFile:
    def __init__(self, edges, distance, filename):
        self.edges = edges
        self.distance = distance
        self.filename = filename

    def save(self):
        if self.compare(self.distance, self.filename) == True:
            with open(self.filename, "w") as f:
                f.write(str(self.distance) + "\n")

                for edge in self.edges:
                    f.write(str(edge) + ",\n")


    def compare(self, distance, filename):
        try:
            with open(filename, "r") as f:
                content = f.readlines()
                try:
                    if int(content[0]) <= distance:
                        return False
                    else:
                        return True
                except:
                    raise TypeError("!!!!ERROR!!!!")
        except:
            return False

    # def textToEdges(self, filename):
    #     edges = []
    #     with open(filename, "r") as f:
    #         content = f.readlines()

    #         for c in content:
    #             try:
    #                 edges.append([float(c)])
    #             except:
    #                 pass
        
    #     return edges