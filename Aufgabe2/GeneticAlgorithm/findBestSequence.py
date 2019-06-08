class FindBestSequence:
    def __init__(self, triangles):
        """
            input: - triangles = list of [smallest_angle, lengths] 
        """
        self.vertex = []
        self.triangles = list(triangles)
        self.len = len(triangles)

    @property
    def finalSequence(self):
        LIMIT = 180
        self.findVertices([], self.triangles, LIMIT) 
        result = self.result
        return result

    def findVertices(self, vertices, numbers, limit=180):
        """
            finds all sequences
            vetices = points where the road and the triangles meet
        """

        self.findSequence(numbers, limit)
        vertices.append(self.vertex)
        
        for v in self.vertex:
            numbers.remove(v)

        if numbers == []:
            self.result = vertices
        else:
            self.findVertices(vertices, numbers, limit)


    def findSequence(self, numbers, limit):
        """
            This function finds a sequence (list of numbers that add up to a specific limit).
            In case this is not excatly possible the limit is graduallly decreased.

            input: - numbers: list of
                   - limit: int
        """

        try:
            next(self.subset_sum(numbers, limit))
        except StopIteration:
            self.findSequence(numbers, (limit - 1))
        else:
            self.vertex = next(self.subset_sum(numbers, limit))

    def subset_sum(self, numbers, target, partial=[], partial_sum=0):
        """
            This recursive function adds elements of a list of numbers up to fit a specified limit (target)
        """

        if partial_sum == target:
            yield partial
        if partial_sum >= target:
            return
        
        for i, n in enumerate(numbers):
            remaining = numbers[i + 1:]
            yield from self.subset_sum(remaining, target, partial + [n], partial_sum + n[0])
