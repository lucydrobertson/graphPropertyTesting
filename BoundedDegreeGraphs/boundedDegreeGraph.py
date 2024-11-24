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
            raise KeyError(f"The vertex {vertex} is not present in the incidence function")

    def add_neighbour(self, vertex, new_neighbour):
        try:
            # add in the new neighbour to an undirected graph
            # iff both the vertex and the new neighbour have space
            if (len(self.inc_func[vertex]) < self.degree and len(self.inc_func[new_neighbour]) <
                    self.degree and not self.directed):
                self.inc_func[new_neighbour].append(vertex)
                self.inc_func[vertex].append(new_neighbour)
            # otherwise if graph is undirected, add in new neighbour if vertex has space
            elif self.directed and len(self.inc_func[vertex]) < self.degree:
                self.inc_func[vertex].append(new_neighbour)
            else:
                raise ValueError("The degree of vertex {vertex} is already bounded by the graph's maximum degree")

        except KeyError:
            raise KeyError(f"The vertex {vertex}  or its neighbour {new_neighbour} is not present in the incidence function")

    def get_size(self):
        return self.size

    def get_degree(self):
        return self.degree

    def get_directed(self):
        return self.directed
