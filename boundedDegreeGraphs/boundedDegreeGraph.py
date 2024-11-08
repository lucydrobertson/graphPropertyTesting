class BoundedDegreeGraph:
    def __init__(self, num_vertices, degree, incidence_function):
        self.size = num_vertices
        self.degree = degree
        self.inc_func = incidence_function

    def get_neighbours(self, vertex):
        try:
            return self.inc_func[vertex]
        except KeyError:
            raise KeyError(f"The vertex {vertex} is not present in the incidence function")

    def add_neighbour(self, vertex, new_neighbour):
        try:
            if len(self.inc_func[vertex]) < self.degree:
                self.inc_func[vertex].append(new_neighbour)
            else:
                raise ValueError("The degree of vertex {vertex} is already bounded by the graph's maximum degree")
        except KeyError:
            raise KeyError(f"The vertex {vertex} is not present in the incidence function")

    def get_size(self):
        return self.size()

    def get_degree(self):
        return self.degree
