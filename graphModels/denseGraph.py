class DenseGraph:
    def __init__(self, num_vertices, adjacency_matrix):
        self.size = num_vertices
        # adj_matrix is a dictionary of dictionaries that represents a symmetric adjacency matrix
        self.adj_matrix = adjacency_matrix

    def is_edge(self, v1, v2) -> bool:
        # adjacency matrix is symmetric so only store each edge once
        # adj_matrix then has a triangular shape
        if v1 < v2:
            return self.adj_matrix[v1][v2]
        else:
            return self.adj_matrix[v2][v1]

    def add_edge(self, v1, v2):
        if v1 < v2:
            self.adj_matrix[v1][v2] = True
        else:
            self.adj_matrix[v2][v1] = True
