import random

from graphModels.denseGraph import DenseGraph


class DenseGraphTester:
    def __init__(self, graph, epsilon):
        self.graph = graph
        self.epsilon = epsilon

    def construct_induced_subgraph(self, vertices):
        num_vertices = len(vertices)
        # construct an empty adjacency matrix
        subgraph_adj_matrix = [[False] * num_vertices for _ in range(num_vertices)]
        # construct the subgraph adjacency matrix from the full graph
        # use x and y so that subgraph has vertices labelled 0 ... n
        for x in range(0, num_vertices):
            for y in range(0, num_vertices):
                subgraph_adj_matrix[x][y] = self.graph.is_edge(vertices[x], vertices[y])
        return DenseGraph(num_vertices, subgraph_adj_matrix)

    def test_bipartiteness(self):
        num_select = int(1/(self.epsilon ** 2))
        vertices_chosen = [random.randrange(0, self.graph.get_size()) for _ in range(num_select)]
        # remove duplicates, unlikely to be many when tester is used on large graph as intended
        vertices_chosen = list(set(vertices_chosen))
        subgraph = self.construct_induced_subgraph(vertices_chosen)

        # perform bfs to decide if subgraph is bipartite
        # 2-col == bipartite
        # start from vertex 0, an arbitrary choice
        queue = [0]
        colouring = {0: 0}
        while len(queue) > 0:
            current = queue.pop(0)
            for n in range(subgraph.get_size()):
                if subgraph.is_edge(current, n):
                    try:
                        # need to ensure node isn't being compared to itself
                        # as it always has an edge of length 0 to itself
                        if current != n and colouring[current] == colouring[n]:
                            return False
                    except KeyError:
                        # if vertex n is not in the dictionary then it's not in the queue
                        queue.append(n)
                        if colouring[current] == 0:
                            colouring[n] = 1
                        else:
                            colouring[n] = 0
        return True

    def test_degree_regularity(self):
        # select 1/e vertices, and estimate degree by making 1/e2 queries each
        # if range is estimates if <= 0.02ev, accept else reject
        num_select = int(1/self.epsilon)
        vertices_chosen = [random.randrange(0, self.graph.get_size()) for _ in range(num_select)]
        vertices_chosen = list(set(vertices_chosen))

        degrees = []

        # estimate degree
        for v1 in vertices_chosen:
            degree = 0
            for v2 in vertices_chosen:
                if self.graph.is_edge(v1, v2):
                    degree += 1
            degrees.append(degree)

        # sort degrees in ascending order
        degrees.sort()
        degree_range = degrees[-1] - degrees[0]
        return degree_range <= 0.02 * self.epsilon * self.graph.get_size()
