class ColouringTester:
    def __init__(self, graph):
        self.graph = graph

    def test_bd_colouring(self, colouring):
        size = self.graph.get_size()
        for v1 in range(0, size):
            for v2 in range(0, size):
                if v1 in self.graph.get_neighbours(v2) or v2 in self.graph.get_neighbours(v1):
                    if colouring[v1] == colouring[v2]:
                        return False
        return True
