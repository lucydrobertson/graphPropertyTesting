import math
import random

from BoundedDegreeGraphs.boundedDegreeGraph import BoundedDegreeGraph
from DenseGraphs.denseGraph import DenseGraph


class GraphGenerator:
    def __init__(self, dense, directed, epsilon=1/6):
        # boolean: True for dense graph, false for bounded degree (sparse) graph
        self.dense = dense
        self.directed = directed
        self.epsilon = epsilon

    # converts a list of edges to a dense graph
    def convert_to_dense(self, graph_size, graph_edges):
        graph = DenseGraph(graph_size, [[False] * graph_size for _ in range(0, graph_size)])
        for edge in graph_edges:
            graph.add_edge(edge[0], edge[1])
            if not self.directed:
                graph.add_edge(edge[1], edge[0])
        return graph

    def convert_to_bounded_degree(self, graph_size, max_degree, graph_edges):
        # create empty graph
        graph = BoundedDegreeGraph(graph_size, max_degree, {}, self.directed)
        for edge in graph_edges:
            graph.add_neighbour(edge[0], edge[1])
        print(graph.inc_func)
        return graph

    def decide_num_edges(self, size):
        # edge generation
        # generate p, the poly factor for the #edges, with a min value of 0.5 to ensure the graph has sufficient edges
        p = random.uniform(0.5, 1)
        if self.dense:
            num_edges = int(p * size ** 2)
        # for a sparse graph, have some p*n*log(n) edges
        else:
            num_edges = int(p * size * math.log2(size))
        return num_edges

    def generate_bipartite_graph(self, size):
        # generate |size| nodes and probabilistically assign them to set a or set b
        # then generate some k * |size|**2 number of edges connecting the two sets
        # idea: maybe have some parameter for degree regularity or some standard deviation from it?
        # idea: have the probability of assignment to set a or b as a new parameter?

        # create an empty graph of size |size|
        bpt_graph_edges = []

        # assign nodes to set a or b probabilistically
        set_a = []
        set_b = []
        for x in range(0, size):
            set_choice = random.choice([True, False])
            if set_choice:
                set_a.append(x)
            else:
                set_b.append(x)

        num_edges = self.decide_num_edges(size)

        for e in range(0, num_edges):
            # for undirected graph, doesn't matter if start is in set_a or set_b
            start = random.choice(set_a)
            end = random.choice(set_b)

            # during graph conversion, adding edges is idempotent
            # so doesn't matter if same (start, end) pair occurs more than once
            bpt_graph_edges.append([start, end])

        if self.dense:
            return self.convert_to_dense(size, bpt_graph_edges)
        else:
            # arbitrarily set max_degree to 5*log2(size of graph)
            # TO DO: decide if this is a good choice, maybe it should be a parameter??
            return self.convert_to_bounded_degree(size, math.log2(size)*5, bpt_graph_edges)

    def generate_k_col_graph(self, size, k):
        k_col_edges = []

        node_sets = [[] for _ in range(0, k)]

        # probabilistically assign nodes to one of the k sets
        for x in range(0, size):
            set_choice = random.randrange(0, k)
            node_sets[set_choice].append(x)

        num_edges = self.decide_num_edges(size)

        for e in range(0, num_edges):
            starting_set, ending_set = random.sample(node_sets, 2)
            start_node = random.choice(starting_set)
            ending_node = random.choice(ending_set)

            k_col_edges.append([start_node, ending_node])

        if self.dense:
            return self.convert_to_dense(size, k_col_edges)
        else:
            # arbitrarily set max_degree to 5*log2(size of graph)
            # TO DO: decide if this is a good choice, maybe it should be a parameter??
            return self.convert_to_bounded_degree(size, math.log2(size)*5, k_col_edges)

    def generate_e_far_from_k_col_graph(self, size, k):
        # similar idea to generating a k-col graph
        # assign nodes to one of k sets and have edges between sets
        # then create a number of violating edges which start and end in the same set
        k_col_edges = []

        node_sets = [[] for _ in range(0, k)]

        # probabilistically assign nodes to one of the k sets
        for x in range(0, size):
            set_choice = random.randrange(0, k)
            node_sets[set_choice].append(x)

        num_edges = self.decide_num_edges(size)
        # number of edges that would need to be removed to make the graph k-colourable
        num_violating_edges = int(self.epsilon * size)

        for _ in range(0, num_edges - num_violating_edges):
            starting_set, ending_set = random.sample(node_sets, 2)
            start_node = random.choice(starting_set)
            ending_node = random.choice(ending_set)

            k_col_edges.append((start_node, ending_node))

        # create the violating edges, that start and end in the same node set
        for _ in range(0, num_violating_edges):
            set_choice = random.randrange(0, k)
            start_edge = random.choice(node_sets[set_choice])
            end_edge = random.choice(node_sets[set_choice])

            k_col_edges.append((start_edge, end_edge))

        if self.dense:
            return self.convert_to_dense(size, k_col_edges)
        else:
            # arbitrarily set max_degree to 5*log2(size of graph)
            # TO DO: decide if this is a good choice, maybe it should be a parameter??
            return self.convert_to_bounded_degree(size, math.log2(size) * 5, k_col_edges)

    def generate_e_far_from_bipartite_graph(self, size):
        return self.generate_e_far_from_k_col_graph(size, 2)

    def generate_degree_regular_graph_edges(self, size, degree):
        # basic idea
        # keep track of the current degree of every node
        # add an edge between any two nodes that aren't yet of the correct degree
        # repeat until every node is of the max degree or there is only one node left (failure??)
        if size < degree + 1 or (size * degree) % 2 == 1:
            raise Exception(f"It is not possible for a graph of size {size} and degree {degree} to be regular")
        else:
            edges = []

            # stores if the current degree of a node
            node_degrees = {n: 0 for n in range(0, size)}

            # stores a list of nodes which haven't reached the max degree
            not_max_degree_nodes = [n for n in range(0, size)]
            while len(not_max_degree_nodes) > 0:
                # pick two random nodes that aren't at max degree
                # by definition of random.sample, node1 != node2
                node1, node2 = random.sample(not_max_degree_nodes, 2)

                edges.append((node1, node2))
                node_degrees[node1] += 1
                node_degrees[node2] += 1

                # remove nodes from not max degree list if they now have the desired degree
                for node in [node1, node2]:
                    if node_degrees[node] == degree:
                        not_max_degree_nodes.remove(node)

                # it is possible that there is one node n left that is not of the desired degree
                # in that case, remove one edge (e1, e2) at random
                # and add new edges (n, e1) and (n, e2)
                # TO DO: prove this works
                if len(not_max_degree_nodes) == 1:
                    leftover_node = not_max_degree_nodes.pop()
                    while node_degrees[leftover_node] < degree:
                        random_edge_index = random.randrange(0, len(edges))
                        # don't want to remove an edge already including leftover node
                        e1, e2 = edges[random_edge_index]
                        if e1 != leftover_node and e2 != leftover_node:
                            # remove the chosen edges from edges
                            edges.pop(random_edge_index)
                            # add in the two new required edges
                            edges.append((e1, leftover_node))
                            edges.append((e2, leftover_node))
                            # update degree of leftover node
                            node_degrees[leftover_node] += 2
        return edges

    def generate_degree_regular_graph(self, size, degree):
        edges = self.generate_degree_regular_graph_edges(size, degree)
        if self.dense:
            return self.convert_to_dense(size, edges)
        else:
            return self.convert_to_bounded_degree(size, degree, edges)

    def generate_e_far_from_degree_regular_graph(self, size, degree):
        # basic idea, generate degree regular graph
        # then remove epsilon*n edges, and choose epsilon*n/d nodes called add
        # for each node in add, add d edges to from it to some other random node
        # until epsilon*n edges have been added
        regular_graph_edges = self.generate_degree_regular_graph_edges(size, degree)

        # removing epsilon * n edges from regular graph
        for _ in range(0, int(self.epsilon * size / degree)):
            regular_graph_edges.pop(random.randrange(0, len(regular_graph_edges)))

        # adding in epsilon * n violating edges
        add = random.sample(range(0, size), int(self.epsilon * size / degree))
        for node in add:
            # pick some other d nodes to add edges to from node
            new_edges = [(node, neighbour) for neighbour in random.sample(range(0, size), degree)]
            regular_graph_edges += new_edges

        if self.dense:
            return self.convert_to_dense(size, regular_graph_edges)
        else:
            return self.convert_to_bounded_degree(size, degree, regular_graph_edges)

    def generate_cycle_free_graph(self, size):
        # if dense, more children is fine, otherwise we want fewer children per node so just use the log value
        if self.dense:
            max_children_per_node = int(size / math.log(size, 2))
        else:
            max_children_per_node = int(math.log(size))

        to_explore = [0]
        edges = []
        num_nodes_explored = 1
        while len(to_explore) > 0 and num_nodes_explored < size:
            current_node = to_explore.pop(0)
            num_children = random.randint(1, max_children_per_node)
            if num_nodes_explored + num_children > size:
                num_children = size - num_nodes_explored
            children = [x for x in range(num_nodes_explored, num_nodes_explored + num_children)]
            for child in children:
                edges.append((current_node, child))
            num_nodes_explored += num_children
            to_explore += children

        # if there is an undirected graph, add in some narrowing (downwards edges)
        if self.directed:
            num_narrowing_edges = random.randint(0, max_children_per_node**2)
            narrowing_edges = []
            for _ in range(0, num_narrowing_edges):
                n1 = random.randint(0, size)
                n2 = random.randint(n1 + 1, size)
                narrowing_edges.append((n1, n2))
            edges += narrowing_edges

        if self.dense:
            return self.convert_to_dense(size, edges)
        else:
            return self.convert_to_bounded_degree(size, max_children_per_node ** 2, edges)
