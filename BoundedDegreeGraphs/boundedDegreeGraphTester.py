import math
from random import randrange, choice

from BoundedDegreeGraphs.boundedDegreeGraph import BoundedDegreeGraph
from create_k_colourings import generate_k_colourings


def test_bd_colouring(graph, colouring):
    for v1 in range(0, graph.get_size()):
        for v2 in range(0, graph.get_size()):
            if v1 in graph.get_neighbours(v2) or v2 in graph.get_neighbours(v1):
                if colouring[v1] == colouring[v2]:
                    return False
    return True


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

        # perform k random walks of length l, starting from vertex v each time
        for x in range(0, k):
            current_vertex = v
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

    def breadth_first_search_find_cycle(self, starting_vertex, max_exploration):
        # return cycle_found:bool, num_vertices_explored: int
        to_explore = [starting_vertex]
        explored = 0

        added = {starting_vertex: starting_vertex}
        # only explore the component up to size max_exploration, then return
        while len(to_explore) > 0 and explored < max_exploration:
            v = to_explore.pop(0)
            neighbours = self.graph.get_neighbours(v)
            # remove the vertex that added v from its neighbours, as it has already been explored
            # and in an undirected graph, it will cause a cycle to be detected when no such cycle exists
            if added[v] in neighbours:
                neighbours.remove(added[v])

            # store that vertex v added all of its neighbours to the to_explore queue
            for n in neighbours:
                added[n] = v

            # add neighbours to list of vertices to explore
            to_explore += neighbours
            explored += 1
            if starting_vertex in neighbours:
                # then we have found a cycle so return True
                return True, explored

        # no cycle found so return False, number of vertices explored
        return False, explored

    def test_cycle_freeness(self):
        # select l = O(1/e3) vertices
        # perform bfs from each vertex s in l, until 8/ed vertices are reached
        # or until no new vertices can be reached
        # if any search finds a cycle, reject
        # else let N be the number of vertices that had a component >= size 8/ed
        # let M = 1/2 sum of degrees of N
        # if (M-N)/L < ed/16 then accept else reject

        vertices_chosen = self.choose_vertices(int(self.graph.get_size() / self.epsilon**3))

        max_exploration = 8 / (self.epsilon * self.graph.get_degree())
        vertices_reached = []
        for s in vertices_chosen:
            cycle_found, vertices_explored = self.breadth_first_search_find_cycle(s, max_exploration)
            if cycle_found:
                return False
            else:
                vertices_reached.append(vertices_explored)

        # max_explored_vertices consists of all vertices chosen that were part of component of max size explored
        max_explored_vertices = list(filter(lambda n: n >= max_exploration, vertices_reached))
        # degree_list stores the degrees of each vertex in max_explored_vertices
        degree_list = [len(self.graph.get_neighbours(v)) for v in max_explored_vertices]

        N = len(max_explored_vertices)
        M = 0.5 * sum(degree_list)
        return (M - N)/len(vertices_chosen) < self.epsilon * self.graph.get_degree() / 16

    def get_vertices_in_radius(self, start_vertex, distance):
        # return a list of all vertices reachable from start_vertex that are at most distance d away
        reachable = {0: [start_vertex]}
        for d in range(0, distance):
            current_neighbours = []
            for vertex in reachable[d]:
                current_neighbours += self.graph.get_neighbours(vertex)
            reachable[d+1] = list(set(current_neighbours))

        # condense dictionary into one list
        vertices_in_radius = [v for k in reachable.keys() for v in reachable[k]]
        # remove duplicates
        vertices_in_radius = list(set(vertices_in_radius))
        return vertices_in_radius

    def create_induced_subgraph(self, subgraph_vertices):
        # return an induced subgraph that only includes the vertices present in subgraph_vertices
        incidence_function = {}
        for vertex in range(0, len(subgraph_vertices)):
            neighbours = self.graph.get_neighbours(subgraph_vertices[vertex])
            # filter neighbours so the list only includes neighbours present in the subgraph
            neighbours = [n for n in neighbours if n in subgraph_vertices]
            # use vertex as dictionary key so that subgraph vertices are labelled 0, 1, 2, ...
            incidence_function[vertex] = neighbours
        return BoundedDegreeGraph(
            len(incidence_function.keys()),
            self.graph.get_degree(),
            incidence_function,
            self.graph.get_directed()
        )

    def test_sparse_k_colourability(self, k):
        # k-colourability tester that works on sparse bounded degree graphs
        # sample a set S of s1 vertices at random
        # for each v in S, Uv = D(v, s2)
        # where D(v, i) is all vertices at distance <= i from v
        # then U = union of the Uv's
        # accept if the subgraph G induced by U satisfies the property

        # picked random constants for now
        s1 = int(self.graph.get_size() / 2)
        s2 = 2

        vertices_chosen = self.choose_vertices(s1)
        subgraph_vertices = []
        for v in vertices_chosen:
            subgraph_vertices += self.get_vertices_in_radius(v, s2)
        subgraph_vertices = list(set(subgraph_vertices))

        subgraph = self.create_induced_subgraph(subgraph_vertices)

        # test if subgraph is k-colourable
        # generate all possible colourings of the subgraph
        # then check if any colouring is k-colourable
        possible_colourings = generate_k_colourings(subgraph.get_size(), k)
        for colouring in possible_colourings:
            if test_bd_colouring(subgraph, colouring):
                return True
        return False