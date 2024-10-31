class DenseGraph:
    def __init__(self, num_vertices, adjacency_matrix):
        self.size = num_vertices
        # adj_matrix is a dictionary of dictionaries that represents an adjacency matrix
        self.adj_matrix = adjacency_matrix

    def is_edge(self, v1, v2) -> bool:
        if v1 == v2:
            return True
        else:
            return self.adj_matrix[v1][v2]

    def add_edge(self, v1, v2):
        self.adj_matrix[v1][v2] = True

    def get_size(self):
        return self.size
