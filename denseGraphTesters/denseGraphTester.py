import random

from graphModels.denseGraph import DenseGraph


class DenseGraphTester:
    def __init__(self, graph, epsilon):
        self.graph = graph
        self.epsilon = epsilon

    def construct_induced_subgraph(self, vertices):
        num_vertices = len(vertices)
        # construct an empty adjacency matrix
        subgraph_adj_matrix = [[False] * num_vertices] * num_vertices
        # construct the subgraph adjacency matrix from the full graph
        for v1 in vertices:
            for v2 in vertices:
                subgraph_adj_matrix[v1][v2] = self.graph.is_edge(v1, v2)
        return DenseGraph(num_vertices, subgraph_adj_matrix)

    def test_bipartiteness(self):
        num_select = 1/(self.epsilon ** 2)
        vertices_chosen = [random.randint(0, self.graph.get_size()) for _ in range(num_select)]
        # remove duplicates by making vertices_chosen a set
        vertices_chosen = set(vertices_chosen)
        subgraph = self.construct_induced_subgraph(vertices_chosen)

        # perform bfs to decide if subgraph is bipartite
        # 2-col == bipartite

