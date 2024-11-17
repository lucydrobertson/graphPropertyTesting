import math
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

