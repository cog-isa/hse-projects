from vertice import Vertice


class Graph():
    def __init__(self):
        self.points = {}

    def add_point(self, name):
        self.points[name] = Vertice(name)

    def add_edge(self, start, destination, weight):
        if start not in self.points:
            self.add_point(start)
        if destination not in self.points:
            self.add_point(destination)
        self.points[start].new_edge(destination, weight)

    def normalize(self):
        for i in self.points:
            outgoing_sum = sum([self.points[i].edges[edge].weight for edge in self.points[i].edges])
            for edge in self.points[i].edges:
                self.points[i].edges[edge].weight = self.points[i].edges[edge].weight/outgoing_sum

    def show(self):
        for point in self.points:
            print point, ':'
            for edge in self.points[point].edges:
                print "\t", edge.destination, ":", edge.weight


def test():
    g = Graph()
    n = 4
    for x in range(n):
        for y in range(n):
            if x != y:
                g.add_edge(x, y, 1)
    g.show()
    g.normalize()
    print
    g.show()