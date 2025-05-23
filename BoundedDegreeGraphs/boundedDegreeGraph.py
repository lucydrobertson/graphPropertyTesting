import networkx as nx
import matplotlib.pyplot as plt


class BoundedDegreeGraph:
    def __init__(self, num_vertices, degree, incidence_function, directed):
        self.size = num_vertices
        self.degree = degree
        self.inc_func = incidence_function
        self.directed = directed

    def get_neighbours(self, vertex):
        try:
            return self.inc_func[vertex]
        except KeyError:
            # return no neighbours if vertex is not in incidence function
            return []

    def add_neighbour(self, vertex, new_neighbour):
        if vertex not in self.inc_func.keys():
            self.inc_func[vertex] = []
        if new_neighbour not in self.inc_func.keys():
            self.inc_func[new_neighbour] = []

        try:
            # add in the new neighbour to an undirected graph
            # iff both the vertex and the new neighbour have space
            if (len(self.get_neighbours(vertex)) < self.degree and len(self.get_neighbours(new_neighbour)) <
                    self.degree and not self.directed):
                self.inc_func[new_neighbour].append(vertex)
                self.inc_func[vertex].append(new_neighbour)
            # otherwise if graph is undirected, add in new neighbour if vertex has space
            elif self.directed and len(self.inc_func[vertex]) < self.degree:
                self.inc_func[vertex].append(new_neighbour)
            else:
                raise ValueError("The degree of vertex {vertex} is already bounded by the graph's maximum degree")

        except KeyError:
            raise KeyError(f"The vertex {vertex}  or its neighbour {new_neighbour} is not present"
                           f" in the incidence function")

    def get_size(self):
        return self.size

    def get_degree(self):
        return self.degree

    def increment_degree(self):
        self.degree += 1

    def get_directed(self):
        return self.directed

    def visualise_graph(self):
        edges = []
        for node, neighbours in self.inc_func.items():
            for neighbour in neighbours:
                edges.append((node, neighbour))
        graph = nx.Graph()
        graph.add_edges_from(edges)
        nx.draw_networkx(graph)
        plt.show()
