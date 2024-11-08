import math
from operator import truediv

from boundedDegreeGraphs.boundedDegreeGraph import BoundedDegreeGraph
from random import randrange, choice


class BoundedDegreeGraphTester:
    def __init__(self, graph, epsilon):
        self.graph = graph
        self.epsilon = epsilon

    def choose_vertices(self, num_to_choose):
        vertices_chosen = [randrange(0, self.graph.get_size()) for _ in range(num_to_choose)]
        # remove duplicates by converting to a set then back to a list
        # note that duplicates become less likely when the testers are used with large graphs as intended
        vertices_chosen = list(set(vertices_chosen))
        return vertices_chosen

    def odd_cycle(self, v):
        n = self.graph.get_size()
        # perform k random walks of length l
        l = int(math.log(n) / self.epsilon)
        k = int(math.sqrt(n) * l)

        reached_from_even = []
        reached_from_odd = []

        current_vertex = v
        for x in range(0, k):
            for path_length in range(1, l + 1):
                # randomly select next vertex from neighbours
                current_vertex = choice(self.graph.get_neighbours(current_vertex))
                # add next hop vertex to reached from even or odd arrays, depending on path length
                if path_length % 2 == 0:
                    reached_from_even.append(current_vertex)
                else:
                    reached_from_odd.append(current_vertex)

        # if a vertex has been found on both an odd and even length path
        # we have an odd length cycle which means the graph is not bipartite
        for even_vertex in reached_from_even:
            if even_vertex in reached_from_odd:
                return True
        return False

    def test_bipartiteness(self):
        # select vertices s O(1/e) times()
        # if odd-cycle(s) returns true then reject
        # k = sqrt(n) * log(n)/e and l = log(n)/e
        # perform k walks starting from s of length l
        # return found if some vertex v is reached from s on both an odd and even length path

        vertices_chosen = self.choose_vertices(int(self.graph.get_size() / self.epsilon))
        for vertex in vertices_chosen:
            if self.odd_cycle(vertex):
                return False
        return True
