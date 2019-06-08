tris = [edges[:3] for _ in range(int(len(edges) / 3))]
        self.coordinates = [set([tuple(point) for edge in t for point in edge]) for t in tris]
        print((self.coordinates))