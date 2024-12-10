import networkx as nx
import matplotlib.pyplot as plt

class DenseGraph:
    def __init__(self, num_vertices, adjacency_matrix):
        self.size = num_vertices
        # adj_matrix is a dictionary of dictionaries that represents an adjacency matrix
        self.adj_matrix = adjacency_matrix

    def is_edge(self, v1, v2) -> bool:
        return self.adj_matrix[v1][v2]

    def add_edge(self, v1, v2):
        self.adj_matrix[v1][v2] = True

    def get_size(self):
        return self.size

    def visualise_graph(self):
        edges = []
        for n1 in range(0, self.size):
            for n2 in range(0, self.size):
                if self.is_edge(n1, n2):
                    edges.append((n1, n2))
        graph = nx.Graph()
        graph.add_edges_from(edges)
        nx.draw_networkx(graph)
        plt.show()
